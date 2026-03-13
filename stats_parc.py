from mrjob.job import MRJob


class MRStatsParc(MRJob):

    def mapper(self, _, line):
        if line.startswith("nom;"):
            return

        parts = line.split(";")
        if len(parts) < 2:
            return

        try:
            production = float(parts[1].strip())
            yield "PARC", (production, production, production, 1)
        except ValueError:
            return

    def reducer(self, key, values):
        min_val = float("inf")
        max_val = float("-inf")
        total = 0.0
        count = 0

        for vmin, vmax, vsum, vcount in values:
            min_val = min(min_val, vmin)
            max_val = max(max_val, vmax)
            total += vsum
            count += vcount

        mean = total / count if count else 0

        yield key, {
            "min": min_val,
            "max": max_val,
            "mean": mean
        }


def run_stats_parc(filename):
    mr_job = MRStatsParc(args=[filename])

    with mr_job.make_runner() as runner:
        runner.run()
        return list(mr_job.parse_output(runner.cat_output()))

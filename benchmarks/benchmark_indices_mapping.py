import json
import os
import tempfile

import nlp
from utils import generate_example_dataset, get_duration


SPEED_TEST_N_EXAMPLES = 500_000

RESULTS_BASEPATH, RESULTS_FILENAME = os.path.split(__file__)
RESULTS_FILE_PATH = os.path.join(RESULTS_BASEPATH, "results", RESULTS_FILENAME.replace(".py", ".json"))


@get_duration
def select(dataset: nlp.Dataset):
    _ = dataset.select(range(0, len(dataset), 2))


@get_duration
def sort(dataset: nlp.Dataset):
    _ = dataset.sort("numbers")


@get_duration
def shuffle(dataset: nlp.Dataset):
    _ = dataset.shuffle()


@get_duration
def train_test_split(dataset: nlp.Dataset):
    _ = dataset.train_test_split(0.1)


@get_duration
def shard(dataset: nlp.Dataset, num_shards=10):
    for shard_id in range(num_shards):
        _ = dataset.shard(num_shards, shard_id)


def benchmark_indices_mapping():
    times = {}
    functions = (select, sort, shuffle, train_test_split, shard)
    with tempfile.TemporaryDirectory() as tmp_dir:
        features = nlp.Features({"text": nlp.Value("string"), "numbers": nlp.Value("float32")})
        dataset = generate_example_dataset(
            os.path.join(tmp_dir, "dataset.arrow"), features, num_examples=SPEED_TEST_N_EXAMPLES
        )
        for func in functions:
            times[func.__name__] = func(dataset)

    with open(RESULTS_FILE_PATH, "wb") as f:
        f.write(json.dumps(times).encode("utf-8"))


if __name__ == "__main__":  # useful to run the profiler
    benchmark_indices_mapping()

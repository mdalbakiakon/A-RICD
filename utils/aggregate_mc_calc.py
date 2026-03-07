import json

def aggregate_mc_scores(output_path, shard_num=8):
    """
    Aggregate MC metrics from multiple shard json files.

    Args:
        output_path (str): base path of output files
        shard_num (int): number of shards

    Returns:
        dict: final aggregated metrics
    """

    total_mc1 = 0.0
    total_mc2 = 0.0
    total_mc3 = 0.0
    total_num = 0

    for i in range(shard_num):

        fn = f"{output_path}_{i}.json"

        with open(fn, "r") as f:
            content = json.load(f)

        num = len(content["question"])

        total_num += num
        total_mc1 += content["total_mc1"] * num
        total_mc2 += content["total_mc2"] * num
        total_mc3 += content["total_mc3"] * num

    final_mc1 = total_mc1 / total_num
    final_mc2 = total_mc2 / total_num
    final_mc3 = total_mc3 / total_num

    return {
        "MC1": final_mc1,
        "MC2": final_mc2,
        "MC3": final_mc3,
    }
def factscore_calcs(fs, topics, generations, out_fn=None):
    out = fs.get_score(topics, generations, gamma=10)
    with open(out_fn, "w") as o:
        o.write(json.dumps(out))
        print("FActScore = %.1f%%" % (100*out["score"]))
        if "init_score" in out:
            print("FActScore w/o length penalty = %.1f%%" % (100*out["init_score"]))
        print("Respond ratio = %.1f%%" % (100*out["respond_ratio"]))
        print("# Atomic facts per valid response = %.1f" % (out["num_facts_per_response"]))
    return out
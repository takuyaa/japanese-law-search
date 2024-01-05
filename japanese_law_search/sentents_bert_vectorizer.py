import json

import numpy as np
import sentents_bert


def main():
    model = sentents_bert.SentenceBertJapanese("sonoisa/sentence-bert-base-ja-mean-tokens-v2")

    with open("./data/raw/himitsu-dogu.txt", "r") as f:
        himitsu_dogus = json.load(f)
    # NOTE: Combine name and description to increase the recall for query
    titles = [
        himitsu_dogu["name"] for himitsu_dogu in himitsu_dogus
    ]
    print("Start BERT encode")
    sentence_embeddings = model.encode(titles, batch_size=32)
    print("End BERT encode")

    print("Start serialization as numpy file")
    np.save("data/output/himitsu_dogu_sentens_vector.npy", sentence_embeddings.cpu().detach().numpy())
    print("End serialization")


if __name__ == "__main__":
    main()

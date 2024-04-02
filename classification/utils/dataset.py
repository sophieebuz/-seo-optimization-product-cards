import pickle
import typing
from pathlib import Path

import psycopg2
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import Dataset
from torchvision.io import read_image


def local_conn() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host="seo-postgres-v2",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="password",
    )
# def local_conn() -> psycopg2.extensions.connection:
#     return psycopg2.connect(
#         host="localhost",
#         port=59123, #53322,
#         dbname="postgres",
#         user="postgres",
#         password="password",
#     )



class WbDataset(Dataset):
    def __init__(self,
                 img_paths,
                 target=None,
                 transform=None):

        self.img_paths = img_paths
        self.target = target
        self.transform = transform

    def __getitem__(self, index):
        img_path = self.img_paths[index]
        img = read_image(str(img_path))

        if self.transform is not None:
            img = self.transform(img)
        if self.target is not None:
            label = self.target[index]
            return img, label

        return img

    def __len__(self):
        return len(self.img_paths)

class Collator:
    def __init__(self, transform=None, mixes=None) -> None:
        self.transform = transform
        self.mixes = mixes

    def __call__(self, batch):
        data, targets = zip(*batch)
        data = torch.stack(data)
        targets = torch.tensor(targets)

        if self.mixes is not None:
            data, target = self.mixes(data, targets)
        if self.transform is not None:
            data = self.transform(data)
        return data, targets


def get_target(db="product_cards.db",
               table="images",
               le: typing.Optional[LabelEncoder] = None,
               label_encoder_pickle_file: Path = Path.cwd() / "data" / "labelencoder.pkl"
               ):
    with local_conn() as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT category FROM {table}")
        query = cursor.fetchall()

    target = [query[i][0] for i in range(len(query))]

    if not le:
        le = LabelEncoder()
        le = le.fit(target)

        label_encoder_pickle_file.unlink(missing_ok=True)

        with open(label_encoder_pickle_file, 'wb') as handle:
            pickle.dump(le, handle, protocol=pickle.HIGHEST_PROTOCOL)

    target_enc = le.transform(target)

    # Соотнесения закодированного таргета и названий категорий
    dict_topic = dict(zip(target, target_enc))
    target2idx = dict(sorted(dict_topic.items(), key=lambda item: item[1]))
    idx2target = dict(zip(target_enc, target))

    return torch.from_numpy(target_enc).long(), target2idx, idx2target


def get_traintestsplit(data_dir, target_enc, SEED, db="product_cards.db", table="images"):
    with local_conn() as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM images")
        query = cursor.fetchall()

    img_paths = [data_dir / "/".join(query[i][1:4]) for i in range(len(query))]

    train_paths, test_paths, ytrain, ytest = train_test_split(img_paths, target_enc,
                                                              test_size=0.1,
                                                              stratify=target_enc,
                                                              random_state=SEED)
    return train_paths, test_paths, ytrain, ytest
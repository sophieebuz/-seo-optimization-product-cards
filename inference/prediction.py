import os
import pickle
from pathlib import Path

import torch
from accelerate import Accelerator
from torch.utils.data import DataLoader
from torchvision.models import MobileNet_V2_Weights, mobilenet_v2

from classification.utils.dataset import WbDataset, get_target
from classification.utils.infer import inference
from classification.utils.model import Model


def user_predict(path_to_file):

    # os.system(f"dvc pull")

    BATCH_SIZE = 1

    accelerator = Accelerator(mixed_precision="no", cpu=True)
    # accelerator = Accelerator(mixed_precision="no")
    device = accelerator.device

    processor = MobileNet_V2_Weights.IMAGENET1K_V2.transforms(
        antialias=True,
    )

    with open(Path.cwd() / "data" / "labelencoder.pkl", 'rb') as file:
        label_encoder = pickle.load(file)

    target_enc, _, idx2target = get_target(le=label_encoder)


    dataset_test = WbDataset(path_to_file, None, processor)

    test_loader = accelerator.prepare_data_loader(DataLoader(dataset_test,
                                                             batch_size=BATCH_SIZE,
                                                             shuffle=False,
                                                             pin_memory=True,)
                                                  )

    pretrain_model = mobilenet_v2(weights=MobileNet_V2_Weights.IMAGENET1K_V2)

    NUM_CLASSES = len(idx2target)

    for param in pretrain_model.parameters():
        param.requires_grad = False

    model = Model(
        module_features=pretrain_model.features,
        num_classes=NUM_CLASSES,
    )
    optimizer = torch.optim.AdamW(
        [
            {"params": model.module_avgpool.parameters(), "lr": 3e-4, "weight_decay": 1e-5},
            {"params": model.out.parameters(), "lr": 3e-4},
        ],
    )
    model, optimizer = accelerator.prepare(model, optimizer)

    accelerator.load_state(Path.cwd() / "data" / "checkpoint_model")
    y_preds = inference(model, test_loader, device)

    return idx2target[y_preds[0]]
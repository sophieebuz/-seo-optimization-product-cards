import pickle
from pathlib import Path

import torch
from accelerate import Accelerator
from torch.utils.data import DataLoader
from torchvision.models import MobileNet_V2_Weights, mobilenet_v2
from utils.dataset import WbDataset, get_target, get_traintestsplit
from utils.infer import inference
from utils.model import Model
from utils.seed import seed_everything, seed_worker


def main() -> None:
    SEED = 13
    seed_everything(SEED)
    g = torch.Generator()
    g.manual_seed(0)

    #os.system(f"dvc pull")

    BATCH_SIZE = 16

    accelerator = Accelerator(mixed_precision="no", cpu=True)
    # accelerator = Accelerator(mixed_precision="no")
    device = accelerator.device

    data_dir = Path.cwd() / "data" / "data"
    processor = MobileNet_V2_Weights.IMAGENET1K_V2.transforms(
        antialias=True,
    )

    with open(Path.cwd() / "data" / "labelencoder.pkl", 'rb') as file:
        label_encoder = pickle.load(file)

    target_enc, _, idx2target = get_target(le=label_encoder)
    _, test_paths, _, ytest = get_traintestsplit(data_dir, target_enc, SEED)

    dataset_test = WbDataset(test_paths, None, processor)

    test_loader = accelerator.prepare_data_loader(DataLoader(dataset_test,
                                                             batch_size=BATCH_SIZE,
                                                             shuffle=False,
                                                             pin_memory=True,
                                                             generator=torch.Generator().manual_seed(SEED),
                                                             worker_init_fn=seed_worker)
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

    return y_preds


if __name__ == "__main__":
    y_preds = main()
    print(y_preds)
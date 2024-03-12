import os
from pathlib import Path

import torch
from accelerate import Accelerator
from torch.utils.data import DataLoader
from torchvision.models import MobileNet_V2_Weights, mobilenet_v2
from utils.dataset import Collator, WbDataset, get_target, get_traintestsplit
from utils.model import Model
from utils.seed import seed_everything, seed_worker
from utils.trainer import Trainer


def main() -> None:
    SEED = 13
    seed_everything(SEED)
    g = torch.Generator()
    g.manual_seed(0)


    #os.system(f"dvc pull {Path.cwd() / 'data' / 'data'}")

    BATCH_SIZE = 16
    NUM_EPOCHS = 10

    accelerator = Accelerator(mixed_precision="no", cpu=True)
    # accelerator = Accelerator(mixed_precision="no")
    device = accelerator.device

    data_dir = Path.cwd() / "data" / "data"
    processor = MobileNet_V2_Weights.IMAGENET1K_V2.transforms(
        antialias=True,
    )

    target_enc, target_mapping = get_target()
    train_paths, test_paths, ytrain, ytest = get_traintestsplit(data_dir, target_enc, SEED)

    train_dataset = WbDataset(train_paths, ytrain, processor)
    test_dataset = WbDataset(test_paths, ytest, processor)

    train_loader = accelerator.prepare_data_loader(DataLoader(train_dataset,
                                                              batch_size=BATCH_SIZE,
                                                              shuffle=True,
                                                              collate_fn=Collator(),
                                                              pin_memory=True,
                                                              generator=torch.Generator().manual_seed(SEED),
                                                              worker_init_fn=seed_worker)
                                                   )

    val_loader = accelerator.prepare_data_loader(DataLoader(test_dataset,
                                                            batch_size=BATCH_SIZE,
                                                            shuffle=False,
                                                            collate_fn=Collator(),
                                                            pin_memory=True,
                                                            generator=torch.Generator().manual_seed(SEED),
                                                            worker_init_fn=seed_worker)
                                                 )

    pretrain_model = mobilenet_v2(weights=MobileNet_V2_Weights.IMAGENET1K_V2)

    NUM_CLASSES = len(target_mapping)

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
    criterion = torch.nn.CrossEntropyLoss().to(device)
    model, optimizer = accelerator.prepare(model, optimizer)

    trainer = Trainer(
        model,
        optimizer,
        None,
        criterion,
        accelerator,
        device,
    )
    train_losses, test_losses, train_metrics, test_metrics = trainer.train(
        train_loader,
        val_loader,
        NUM_EPOCHS,
        plot=False,
        path_for_save= Path.cwd() / "data"
    )


if __name__ == "__main__":
    main()
import numpy as np
import torch


@torch.no_grad()
def inference(model, loader, device):
    model.eval()
    y_preds = []
    for data in loader:
        data = data.to(device)
        logits = model(data)
        y_pred = np.argmax(logits.detach().cpu().numpy(), axis=-1)

        y_preds.extend(y_pred)
    return y_preds
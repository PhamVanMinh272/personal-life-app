# import os
# import torch
# from PIL import Image
# import numpy as np
# from torchvision import transforms
# from src.services.u2net.model import U2NET  # from U-2-Net repo


def remove_background(image_path, output_path):
    # check path exist or not /saved_models/u2net/u2net.pth
    # if not os.path.exists("services/u2net/u2net.pth"):
    #     raise FileNotFoundError(
    #         "Model weights not found at 'services/u2net/u2net.pth'. Please download the U-2-Net model weights and place them in the specified directory."
    #     )
    # net = U2NET(3, 1)
    # net.load_state_dict(torch.load("services/u2net/u2net.pth", map_location="cpu"))
    # net.eval()
    #
    # transform = transforms.Compose(
    #     [
    #         transforms.Resize((320, 320)),
    #         transforms.ToTensor(),
    #         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    #     ]
    # )
    #
    # image = Image.open(image_path).convert("RGB")
    # input_tensor = transform(image).unsqueeze(0)
    #
    # with torch.no_grad():
    #     d1, *_ = net(input_tensor)
    #     mask = d1.squeeze().cpu().numpy()
    #     mask = (mask - mask.min()) / (mask.max() - mask.min())
    #     mask = Image.fromarray((mask * 255).astype(np.uint8)).resize(image.size)
    #
    # # Apply mask to image
    # # image_np = np.array(image)
    # # mask_np = np.array(mask) / 255.0
    # # result = image_np * mask_np[..., None]
    # # result = Image.fromarray(result.astype(np.uint8))
    # # result.save(output_path)
    #
    # # Apply mask to image and composite over white background
    # image_np = np.array(image).astype(np.float32)
    # mask_np = np.array(mask).astype(np.float32) / 255.0
    # alpha = mask_np[..., None]  # shape (H, W, 1)
    # white = 255.0
    # result_np = image_np * alpha + white * (1.0 - alpha)
    # result = Image.fromarray(result_np.astype(np.uint8)).convert("RGB")
    # result.save(output_path)
    pass


# Example usage
# remove_background('input.jpg', 'output.png')

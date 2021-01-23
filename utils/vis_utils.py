from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import torch
from tqdm import tqdm


def imshow(inp, title=None, denormalize=False):
    """
    Reshape a tensor of image data to a grid for easy visualization.

    Inputs:
    - inp: Data of shape (C X H X W)
    - title: Default None
    - denormalize: indicator for inversing transformation, False by default
    """

    # reorder axes to move the channel dimension (H X W X C) instead of (C X H X W)
    inp = inp.numpy().transpose((1, 2, 0))

    # multiply by std and add the mean (i.e. inverse the transform)
    # Mean and Std will be updated based on transform function
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    if denormalize:
        inp = std * inp + mean

        # make sure all numbers are between 0 and 1
        inp = np.clip(inp, 0, 1)

    # plot the image and add the title
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated

    def visualize_output(test_images, test_outputs, gt_pts=None, batch_size=10):
        """
        Visualize the output of the prediction.
        By default this shows a batch of 10 images
        """

        #######################################################################
        # Implement later
        #######################################################################

        pass


def plot_embeddings(embeddings, targets, xlim=None, ylim=None):
    if torch.cuda.is_available():
        embeddings = embeddings.cpu()
        targets = targets.cpu()

    data = pd.DataFrame(
        {"dim_1": embeddings[:, 0], "dim_2": embeddings[:, 1], "targets": targets}
    )
    data["targets"] = data["targets"].astype(
        str
    )  # convert to string, so plotly interprets it as categorical variable

    fig = px.scatter(data, x="dim_1", y="dim_2", color="targets")
    return fig


def extract_embeddings(dataloader, model):
    if torch.cuda.is_available():
        model = model.cuda()

    with torch.no_grad():
        model.eval()

        embeddings = torch.empty(0)
        labels = torch.empty(0)

        print(len(dataloader))

        images, labels = next(iter(dataloader))
        if torch.cuda.is_available():
            images.cuda()
        embeddings = model(images)

        return embeddings.numpy(), labels.numpy()


def extract_embeddings_withoutzeros(dataloader, model):
    with torch.no_grad():
        model.eval()
        embeddings_list = []
        labels_list = []
        for images, target in tqdm(dataloader, total=len(dataloader)):
            if torch.cuda.is_available():
                images = images.cuda()
            embeddings_list.append(model(images).data.cpu().numpy())
            labels_list.append(target.numpy())

        flat_list_l = []
        for sublist in labels_list:
            for item in sublist:
                flat_list_l.append(item)
        labels = np.array(flat_list_l)

        flat_list_e = []
        for sublist in embeddings_list:
            for item in sublist:
                flat_list_e.append(item)
        embeddings = np.array(flat_list_e)

        print(embeddings.shape, labels.shape)

    return embeddings, labels

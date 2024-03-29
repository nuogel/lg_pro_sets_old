"""IOU calculation between box1 and box2, box can be any shape."""
import torch


def iou_mat(box1, box2):
    """
    IOU calculation between box1 and box2,in the shape of [x1 y1 x2 y2].

    :param box1:in the shape of [x1 y1 x2 y2]
    :param box2:in the shape of [x1 y1 x2 y2]
    :return:IOU of boxes1, boxes2
    """
    if len(box1.shape) == 1:
        box1 = box1.view(1, box1.shape[0])
    if len(box2.shape) == 1:
        box2 = box2.view(1, box2.shape[0])
    ious = torch.zeros((box2.shape[0],) + box1.shape[:-1]).cuda()
    for i in range(box2.shape[0]):
        box2_ = box2[i]
        box_tmp = {}
        area1 = (box1[..., 2] - box1[..., 0]) * (box1[..., 3] - box1[..., 1])
        area2 = (box2_[..., 2] - box2_[..., 0]) * (box2_[..., 3] - box2_[..., 1])
        #
        box_tmp['x1'] = torch.max(box1[..., 0], box2_[..., 0])
        box_tmp['y1'] = torch.max(box1[..., 1], box2_[..., 1])
        box_tmp['x2'] = torch.min(box1[..., 2], box2_[..., 2])
        box_tmp['y2'] = torch.min(box1[..., 3], box2_[..., 3])
        box_w = (box_tmp['x2'] - box_tmp['x1'])
        box_h = (box_tmp['y2'] - box_tmp['y1'])
        intersection = box_w * box_h
        ious[i] = intersection / (area1 + area2 - intersection)
        #
        mask1 = (box1[..., 0] + box1[..., 2] - box2_[..., 2] - box2_[..., 0]).abs()\
            - (box1[..., 2] - box1[..., 0] + box2_[..., 2] - box2_[..., 0])
        mask1 = (mask1 < 0).cuda().float()
        mask2 = (box1[..., 1] + box1[..., 3] - box2_[..., 3] - box2_[..., 1]).abs()\
            - (box1[..., 3] - box1[..., 1] + box2_[..., 3] - box2_[..., 1])
        mask2 = (mask2 < 0).cuda().float()
        #
        ious[i] = ious[i] * mask1 * mask2
    return ious


def iou_xywh(boxes1, boxes2):
    """
    IOU calculation between box1 and box2,which is in the shape of [x y w h].

    :param boxes1:in the shape of [x y w h]
    :param boxes2:in the shape of [x y w h]
    :return:IOU of boxes1, boxes2
    """
    ious = iou_mat(xywh2xyxy(boxes1), xywh2xyxy(boxes2))
    return ious


def xywh2xyxy(boxes_xywh):
    """
    Convert boxes with the shape xywh to x1y1x2y2.
    """

    boxes_xyxy = torch.cat([boxes_xywh[..., :2] - boxes_xywh[..., 2:] / 2.0,
                          boxes_xywh[..., :2] + boxes_xywh[..., 2:] / 2.0], -1)
    return boxes_xyxy



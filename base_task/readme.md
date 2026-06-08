### I forgot to add a few annotations in the notebook, so I'll update here, in addition to those already present in the notebook.

- I've split the dataset into 85/15 for training and validation respectively.
- I've resized the image pixels, divided by 255 in order to range them between 0 and 1, to have smaller weights and speed up learning.
- My transform consists of simple tensor-ing (real word?) and normalizing

### Here are the metrics yanked from the notebook:

| Data | Value |
| --- | --- |
| Final Training Loss: | 0.3151253116138307 |
| Final Validation Loss: | 0.3560675010085106 |
| Final Training Accuracy: | 88.43% |
| Final Validation Accuracy: | 87.17% |

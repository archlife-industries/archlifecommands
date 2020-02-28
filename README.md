# archlife
archlife.org/archlife/demo

When a user clicks to record their EEG signals for one second, it initiate this Python API. This Python API connects to the EEG device, reads EEG signals for x-time, creates a pandas dataframe, runs predictions through a pre-trained model, and outputs a command to the front-end for it to respond accordingly according to the command that the user thought with their mind.

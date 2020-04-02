from datetime import datetime
import os
import numpy as np


def configuration():
    seed = 1220
    deterministic = False
    id = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    log_path = os.path.join('..', 'experiment_logs', id)

    #####################
    # quick configuration, uses default parameters of more detailed configuration
    #####################

    machine_type = 5
    machine_id = 0

    batch_size = 512

    epochs = 100
    num_workers = 0

    learning_rate = 1e-4
    weight_decay = 1e-4

    rho = 0.1

    feature_context = 'short'
    reconstruction_class = 'reconstructions.AUC'
    mse_weight = 0.0
    model_class = 'models.BaselineFCNN'

    ########################
    # detailed configurationSamplingFCAE
    ########################

    if feature_context == 'short':
        context = 5
        num_mel = 128
        n_fft = 1024
        hop_size = 512
    elif feature_context == 'long':
        context = 11
        num_mel = 40
        n_fft = 512
        hop_size = 256

    if model_class == 'models.SamplingCRNNAE':
        context = 1

    data_set = {
        'class': 'data_sets.MCMDataSet',
        'kwargs': {
            'context': context,
            'num_mel': num_mel,
            'n_fft': n_fft,
            'hop_size': hop_size
        }
    }

    reconstruction = {
        'class': reconstruction_class,
        'kwargs': {
            'weight': 1.0,
            'input_shape': '@data_set.observation_shape',
            'rho': rho,
            'mse_weight': mse_weight
        }
    }

    model = {
        'class': model_class,
        'args': [
            '@data_set.observation_shape',
            '@reconstruction'
        ]
    }

    lr_scheduler = {
        'class': 'torch.optim.lr_scheduler.StepLR',
        'args': [
            '@optimizer',
        ],
        'kwargs': {
            'step_size': 50
        }
    }

    optimizer = {
        'class': 'torch.optim.Adam',
        'args': [
            '@model.parameters()'
        ],
        'kwargs': {
            'lr': learning_rate,
            'betas': (0.9, 0.999),
            'amsgrad': False,
            'weight_decay': weight_decay,
        }
    }

    trainer = {
        'class': 'trainers.PTLTrainer',
        'kwargs': {
            'max_epochs': epochs,
            'checkpoint_callback': False,
            'logger': False,
            'early_stop_callback': False,
            'gpus': [0],
            'show_progress_bar': True,
            'progress_bar_refresh_rate': 1000
        }
    }
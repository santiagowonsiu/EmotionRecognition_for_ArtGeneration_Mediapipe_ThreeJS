"""General-purpose test script for image-to-image translation.

Once you have trained your model with train.py, you can use this script to test the model.
It will load a saved model from --checkpoints_dir and save the results to --results_dir.

It first creates model and dataset given the option. It will hard-code some parameters.
It then runs inference for --num_test images and save results to an HTML file.

Example (You need to train models first or download pre-trained models from our website):
    Test a CycleGAN model (both sides):
        python test.py --dataroot ./datasets/maps --name maps_cyclegan --model cycle_gan

    Test a CycleGAN model (one side only):
        python test.py --dataroot datasets/horse2zebra/testA --name horse2zebra_pretrained --model test --no_dropout

    The option '--model test' is used for generating CycleGAN results only for one side.
    This option will automatically set '--dataset_mode single', which only loads the images from one set.
    On the contrary, using '--model cycle_gan' requires loading and generating results in both directions,
    which is sometimes unnecessary. The results will be saved at ./results/.
    Use '--results_dir <directory_path_to_save_result>' to specify the results directory.

    Test a pix2pix model:
        python test.py --dataroot ./datasets/facades --name facades_pix2pix --model pix2pix --direction BtoA

See options/base_options.py and options/test_options.py for more test options.
See training and test tips at: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/tips.md
See frequently asked questions at: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/qa.md
"""
import os
from data import create_dataset
from models import create_model
from util import html
import util.util as util
import sys
import json
from argparse import Namespace
import numpy as np
from torchvision.transforms import ToPILImage

# Create the directory if it doesn't exist
os.makedirs('gen_image_png', exist_ok=True)

if __name__ == '__main__':
    # Define the Namespace object
    opt = Namespace(dataroot='./cut_master/datasets/afhq/cat2dog/',
                    name='cat2dog_fastcut_pretrained',
                    easy_label='experiment_name',
                    gpu_ids=[],
                    checkpoints_dir='./checkpoints',
                    model='cut',
                    input_nc=3,
                    output_nc=3,
                    ngf=64,
                    ndf=64,
                    netD='basic',
                    netG='resnet_9blocks',
                    n_layers_D=3, normG='instance',
                    normD='instance', init_type='xavier',
                    init_gain=0.02,
                    no_dropout=True,
                    no_antialias=False,
                    no_antialias_up=False,
                    dataset_mode='unaligned',
                    direction='AtoB',
                    serial_batches=False,
                    num_threads=4,
                    batch_size=1,
                    load_size=256,
                    crop_size=256,
                    max_dataset_size=float('inf'),
                    preprocess='resize_and_crop',
                    no_flip=False,
                    display_winsize=256,
                    random_scale_max=3.0,
                    epoch='latest',
                    verbose=False,
                    suffix='',
                    stylegan2_G_num_downsampling=1,
                    results_dir='./results/',
                    phase='test',
                    eval=False,
                    num_test=500,
                    CUT_mode='FastCUT',
                    lambda_GAN=1.0,
                    lambda_NCE=10.0,
                    nce_idt=False,
                    nce_layers='0,4,8,12,16',
                    nce_includes_all_negatives_from_minibatch=False,
                    netF='mlp_sample',
                    netF_nc=256,
                    nce_T=0.07,
                    num_patches=256,
                    flip_equivariance=True, pool_size=0,
                    n_epochs=150,
                    n_epochs_decay=50,
                    isTrain=False)

    # hard-code some parameters for test
    opt.num_threads = 0   # test code only supports num_threads = 1
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    train_dataset = create_dataset(util.copyconf(opt, phase="train"))
    model = create_model(opt)      # create a model given opt.model and other options
    # create a webpage for viewing the results
    web_dir = os.path.join(opt.results_dir, opt.name, '{}_{}'.format(opt.phase, opt.epoch))  # define the website directory
    print('creating web directory', web_dir)
    webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.epoch))

    for i, data in enumerate(dataset):
        if i == 0:
            model.data_dependent_initialize(data)
            model.setup(opt)               # regular setup: load and print networks; create schedulers
            model.parallelize()
            if opt.eval:
                model.eval()
        if i >= opt.num_test:  # only apply our model to opt.num_test images.
            break
        model.set_input(data)  # unpack data from data loader
        model.test()           # run inference
        visuals = model.get_current_visuals()  # get image results

        # Print keys, shapes, and data types
        for k, v in visuals.items():
            print(f"Key: {k}, Shape: {v.shape}, Data type: {v.dtype}")

        # Convert tensors to PIL images and save them
        to_pil = ToPILImage()
        for k, v in visuals.items():
            image = to_pil(v.squeeze(0).cpu())  # remove the batch dimension
            image.save(os.path.join('gen_image_png', f'{k}.png'))


        # img_path = model.get_image_paths()     # get image paths
    #     if i % 5 == 0:  # save images to an HTML file
    #         print('processing (%04d)-th image... %s' % (i, img_path))
    #     save_images(webpage, visuals, img_path, width=opt.display_winsize)
    # webpage.save()  # save the HTML




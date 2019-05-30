class config(object):
    # train lstm model with fake data
    pretrain_step = 20
    # train lstm model with read dataset
    training_step = 50
    # output file name
    output_file = "output.csv"
    # threshold used in system
    threshold = 0.8
    # dataset used for training
    data_dir = "./data"
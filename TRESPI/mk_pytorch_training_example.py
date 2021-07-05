"""This modules trains a Baseline model.

Start training with this command:
`python train.py <train_encodings_filename>

Set number of EPOCHS and batch size by changing constants near top of
file.

Disable GPU by setting GPU constant at top of file to False.
"""
import datetime
import logging
import os
import pickle
import sys

import torch
import torch.utils.data
import transformers as hft

sys.path.insert(0, "/home/jupyter")
import util.log
import util.data


MODEL_NAME = "distilbert-base-uncased"
TRAIN_DATA = "train_data_28Nov_distilbert.pickle"

EPOCHS = 5
BATCH_SIZE = 32 
LEARNING_RATE = 1e-5
WEIGHTS = [1, 4]
GPU = True

BATCH_REPORT_FREQ = 10 # Loss will be logged every batch if equal to 1,
                       # every other batch if equal to 2, etc.
# Set CHECKPOINT_FILE to None to load untuned model from Huggingface.
# Otherwise set to name of model checkpoint file.
# Checkpoint file should contain dictionary with this format:
#   checkpoint = {"epoch": epoch, "model": model.state_dict(), "optimizer": optim.state_dict()}
CHECKPOINT_FILE = "saved_model_epoch5_20201129_0308.tar"
MAX_BATCH = None       # Used for testing. If not None, only MAX_BATCH
                       # batches will be completed for each epoch.
                                                  

def train():
    # Set up logging
    logger = util.log.get("train_baseline_distilbert_gcpf")
    logger.info("Starting Training")
    
    # Load training data
    with open(TRAIN_DATA, "rb") as dfile:
        train_dataset = pickle.load(dfile)
    logger.info(f"Loaded dataset from: {TRAIN_DATA}")
    logger.info(f"Number of records: {len(train_dataset)}")
    
    # Load Model
    logger.info(f"Loading model: {MODEL_NAME}")
    model = hft.DistilBertForSequenceClassification.from_pretrained(
                MODEL_NAME)  
    
    # Load model state from file
    prior_epochs = 0
    if CHECKPOINT_FILE is not None:
        logger.info(f"Updating model state from file {CHECKPOINT_FILE}.")
        logger.info(f"Current Directory{os.getcwd()}")
        checkpoint = torch.load(CHECKPOINT_FILE)
        model.load_state_dict(checkpoint["model"])
        prior_epochs = checkpoint['epoch']
        logger.info(f"Model has been trained for {prior_epochs} epochs.")
        
    logger.info("Moving model to device")
    device = (torch.device('cuda') if (torch.cuda.is_available() and GPU)
              else torch.device('cpu'))
    logger.info(f"Device: {device}")
    model.to(device)
    
    optim = hft.AdamW(model.parameters(), lr=LEARNING_RATE)
    logger.info(f"Learning Rate: {LEARNING_RATE}")
    if CHECKPOINT_FILE is not None:
        logger.info(f"Updating optimizer state from file {CHECKPOINT_FILE}.")
        optim.load_state_dict(checkpoint["optimizer"])
        del checkpoint

    model.train()
    # Create data loader
    train_loader = torch.utils.data.DataLoader(train_dataset,
                                               batch_size=BATCH_SIZE,
                                               shuffle=True)
                
    logger.info("Commencing Training")
    batches_per_epoch = len(train_dataset)/train_loader.batch_size
    logger.info(f"Batches per Epoch: {batches_per_epoch}")
    gpu_mem = torch.cuda.get_device_properties(0).total_memory/1_049_000_000
    logger.info(f"Total GPU memory available (MiB): {gpu_mem}")
    
    if WEIGHTS is not None:
        criterion = torch.nn.CrossEntropyLoss(weight=torch.Tensor(WEIGHTS).to(device))
    else:
        criterion = torch.nn.CrossEntropyLoss()
    logger.info(f"Cross Entropy Loss Weights: {WEIGHTS}")
    
    start_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    
    for epoch in range(1 + prior_epochs, EPOCHS + 1 + prior_epochs):
        logger.info(f"Starting Epoch {epoch}, " +
                    f"logging every {BATCH_REPORT_FREQ} batches")
        loss_sum = 0
        
        for batch_num, batch in enumerate(train_loader):
            optim.zero_grad()
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            outputs = model(input_ids,
                            attention_mask=attention_mask,
                            labels=labels,
                            output_hidden_states=False, 
                            output_attentions=False)
            loss = criterion(outputs[1], labels)
            loss_sum += loss
            loss.backward()
            optim.step()
            
            print(f"Epoch: {epoch}, Batch: {batch_num + 1}, loss: {loss}")
            if (batch_num + 1) % BATCH_REPORT_FREQ == 0:
                mean_loss = loss_sum / BATCH_REPORT_FREQ
                loss_sum = 0
                logger.info(f"Epoch: {epoch}, Batch: {batch_num + 1}, mean_loss: {mean_loss}")
            
            if MAX_BATCH is not None:  # Used to stop early during testing.
                if batch_num >= MAX_BATCH:
                    break
        
        logger.info(f"Completed {epoch} epochs.")
        saved_checkpoint = {"epoch": epoch,
                            "model": model.state_dict(),
                            "optimizer": optim.state_dict(),
                            "train_encodings_file": TRAIN_DATA,
                            "model_name": MODEL_NAME,
                            "batch_size": BATCH_SIZE,
                            "learning_rate": LEARNING_RATE,
                            "final_batch_loss": loss

        }
        saved_fname = f"saved_model_epoch{epoch}_" + start_time + ".tar"
        torch.save(saved_checkpoint, saved_fname)
        logger.info(f"Saved model in file {saved_fname}")

                
if __name__ == "__main__":
    train()
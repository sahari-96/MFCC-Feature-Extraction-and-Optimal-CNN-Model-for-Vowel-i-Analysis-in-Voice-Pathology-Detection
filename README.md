# MFCC-Feature-Extraction-and-Optimal-CNN-Model-for-Vowel-i-Analysis-in-Voice-Pathology-Detection

#Project Overview

This project explores the analysis of the vowel /i/ using the AVFAD dataset. The objective is to extract 20 Mel-Frequency Cepstral Coefficient (MFCC) features and classify the data using an optimized Convolutional Neural Network (CNN) model. The ultimate goal was to achieve high classification accuracy while minimizing the model's parameters.

#Dataset

The dataset used for this project is the AVFAD dataset, specifically focusing on the vowel /i/. This dataset is widely recognized for its application in speech analysis and voice pathology detection.

#Methodology

1. MFCC Feature Extraction

The first step was extracting 20 MFCC features from the audio samples of the vowel /i/. MFCCs are well-suited for speech analysis as they represent the short-term power spectrum of sound, capturing the essential features required for classification tasks.

2. CNN Model Development

Initially, we used the CNN architecture employed in our previous project, "Voice Pathology Detection by Vowel /a/". While effective, this model was parameter-heavy. To optimize performance:

Baseline Model:

Three convolutional layers with filters: 16, 32, 64.

Dense layer with 128 neurons.

Optimized CNN Model:

Reduced the number of filters in convolutional layers to 8, 16, and 32, respectively.

Reduced the dense layer to 64 neurons.

Maintained model depth and overall architecture to ensure accuracy while reducing computational complexity.

3. Training and Evaluation

Performance metrics included validation accuracy and test accuracy.

All runs were conducted using a T4 GPU on Google Colab, ensuring efficient model training and evaluation.

#Results

The optimized CNN model achieved the following results:

Test Accuracy: 0.8943

Validation Accuracy: 0.8857

This performance represents a significant improvement in computational efficiency while maintaining competitive accuracy in the domain of speech analysis.

#Significance

This project demonstrates the potential of optimized CNN architectures in speech analysis tasks, making models more suitable for real-world applications where computational resources are limited. The methodology and results can be a foundation for future research in voice pathology detection and similar fields.




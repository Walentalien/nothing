import os
import sys
import matplotlib.pyplot as plt

# Create images directory if it doesn't exist
os.makedirs('data/images', exist_ok=True)

# Add the project root to the path to import the modules
sys.path.append('.')

try:
    # Import the ImageGenerator
    from utils.image_generator import ImageGenerator
    
    # Print welcome message
    print("=== VirtualDoctor - Medical Imaging Demo ===")
    print("Demonstrating the Phase 3 medical imaging features...")
    
    # Generate sample ECG image
    print("\nGenerating ECG image...")
    ecg_path = ImageGenerator.generate_ecg(
        patient_id="demo001", 
        heart_rate=90, 
        abnormal=True
    )
    print(f"ECG image generated at: {ecg_path}")
    
    # Generate sample chest X-ray
    print("\nGenerating Chest X-ray image...")
    xray_path = ImageGenerator.generate_chest_xray(
        patient_id="demo001", 
        condition="pneumonia"
    )
    print(f"Chest X-ray image generated at: {xray_path}")
    
    # Generate sample blood test results
    print("\nGenerating blood test results...")
    blood_results = ImageGenerator.generate_blood_test_results(
        patient_id="demo001", 
        condition="infection"
    )
    
    # Display some of the blood test results
    print("\nSample Blood Test Results:")
    for test, data in list(blood_results.items())[:5]:
        if isinstance(data, dict) and 'value' in data:
            value = data['value']
            unit = data.get('unit', '')
            abnormal = data.get('abnormal', False)
            status = "ABNORMAL" if abnormal else "normal"
            print(f"  {test}: {value} {unit} ({status})")
    
    # Display the ECG image
    print("\nDisplaying the ECG image...")
    try:
        ecg_img = plt.imread(ecg_path)
        plt.figure(figsize=(10, 4))
        plt.imshow(ecg_img)
        plt.axis('off')
        plt.title("Generated ECG with Abnormalities")
        plt.savefig('data/images/ecg_display.png')
        print("ECG image saved as: data/images/ecg_display.png")
    except Exception as e:
        print(f"Error displaying ECG image: {e}")
    
    # Display the X-ray image
    print("\nDisplaying the Chest X-ray image...")
    try:
        xray_img = plt.imread(xray_path)
        plt.figure(figsize=(8, 10))
        plt.imshow(xray_img)
        plt.axis('off')
        plt.title("Generated Chest X-ray with Pneumonia")
        plt.savefig('data/images/xray_display.png')
        print("X-ray image saved as: data/images/xray_display.png")
    except Exception as e:
        print(f"Error displaying X-ray image: {e}")
    
    print("\nDemo completed successfully!")
    print("\nThese images would be integrated into the patient tests in the full game.")
    print("When a doctor runs an ECG or X-ray test, these images are generated")
    print("based on the patient's condition and symptoms.")

except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running this script from the project root directory.")
except Exception as e:
    print(f"An error occurred: {e}")
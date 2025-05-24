import os
import random
import math
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class ImageGenerator:
    """Generates medical images for the VirtualDoctor game."""
    
    @staticmethod
    def ensure_dir(directory: str) -> None:
        """Ensure directory exists."""
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    @staticmethod
    def generate_ecg(patient_id: str, heart_rate: int, abnormal: bool = False) -> str:
        """
        Generate an ECG (electrocardiogram) image.
        
        Args:
            patient_id: Patient ID to include in filename
            heart_rate: Heart rate to simulate (beats per minute)
            abnormal: Whether to generate abnormal patterns
            
        Returns:
            Path to generated image file
        """
        # Ensure directory exists
        image_dir = os.path.join('data', 'images')
        ImageGenerator.ensure_dir(image_dir)
        
        # Create a unique filename
        import time
        timestamp = int(time.time())
        filename = f"ecg_{patient_id}_{timestamp}.png"
        filepath = os.path.join(image_dir, filename)
        
        # Set up the plot
        plt.figure(figsize=(10, 4))
        
        # Generate ECG data
        # Time values (in seconds) - 10 seconds of data
        t = np.linspace(0, 10, 1000)
        
        # Calculate frequency based on heart rate
        # Heart rate is in BPM, convert to Hz (cycles per second)
        freq = heart_rate / 60
        
        # Basic normal ECG waveform
        ecg = np.zeros_like(t)
        
        # Generate each heartbeat
        for i, time in enumerate(t):
            # Determine which phase of the heartbeat we're in
            phase = (time * freq) % 1.0  # Normalized phase between 0 and 1
            
            if phase < 0.05:  # P wave
                ecg[i] = 0.25 * np.sin(phase * 2 * np.pi / 0.05)
            elif phase < 0.15:  # PR segment
                ecg[i] = 0
            elif phase < 0.2:  # QRS complex
                if phase < 0.17:  # Q
                    ecg[i] = -0.5 * np.sin((phase - 0.15) * 2 * np.pi / 0.05)
                elif phase < 0.18:  # R
                    ecg[i] = 1.5 * np.sin((phase - 0.17) * 2 * np.pi / 0.02)
                else:  # S
                    ecg[i] = -0.5 * np.sin((phase - 0.18) * 2 * np.pi / 0.04)
            elif phase < 0.4:  # ST segment
                ecg[i] = 0
            elif phase < 0.5:  # T wave
                ecg[i] = 0.35 * np.sin((phase - 0.4) * 2 * np.pi / 0.1)
            else:  # Baseline
                ecg[i] = 0
        
        # Add abnormalities if needed
        if abnormal:
            # Choose a random abnormality type
            abnormality_type = random.choice([
                "st_elevation",  # ST elevation (possible infarction)
                "st_depression",  # ST depression (possible ischemia)
                "long_qt",  # Long QT interval
                "arrhythmia",  # Arrhythmia (irregular heartbeat)
                "pvc"  # Premature ventricular contraction
            ])
            
            if abnormality_type == "st_elevation":
                # Elevate the ST segment
                for i, time in enumerate(t):
                    phase = (time * freq) % 1.0
                    if 0.2 < phase < 0.4:  # ST segment
                        ecg[i] += 0.2
            
            elif abnormality_type == "st_depression":
                # Depress the ST segment
                for i, time in enumerate(t):
                    phase = (time * freq) % 1.0
                    if 0.2 < phase < 0.4:  # ST segment
                        ecg[i] -= 0.2
            
            elif abnormality_type == "long_qt":
                # Increase the QT interval
                for i, time in enumerate(t):
                    phase = (time * freq) % 1.0
                    if 0.4 < phase < 0.5:  # T wave
                        # Shift the T wave later
                        shifted_phase = (phase - 0.1)
                        if 0.4 < shifted_phase < 0.5:
                            ecg[i] = 0.35 * np.sin((shifted_phase - 0.4) * 2 * np.pi / 0.1)
            
            elif abnormality_type == "arrhythmia":
                # Add random variations to the heart rate
                t_new = np.zeros_like(t)
                for i in range(len(t)):
                    if i > 0:
                        # Random variation in time between beats
                        t_new[i] = t_new[i-1] + (t[i] - t[i-1]) * random.uniform(0.7, 1.3)
                    else:
                        t_new[i] = t[i]
                
                # Interpolate the ECG to the new time points
                from scipy.interpolate import interp1d
                f = interp1d(t, ecg, kind='cubic', fill_value="extrapolate")
                ecg = f(t_new)
            
            elif abnormality_type == "pvc":
                # Add PVCs at random locations
                num_pvcs = random.randint(2, 5)
                for _ in range(num_pvcs):
                    # Choose a random location
                    pvc_idx = random.randint(100, len(t) - 100)
                    # Generate PVC waveform (a large, wide QRS complex)
                    width = 30  # Width of the PVC in samples
                    height = 2.0  # Height of the PVC
                    for j in range(-width, width):
                        if 0 <= pvc_idx + j < len(ecg):
                            if j < 0:
                                ecg[pvc_idx + j] = -0.3 * height * np.exp(-(j/10)**2)
                            else:
                                ecg[pvc_idx + j] = height * np.exp(-(j/15)**2) * (-1 if j > 10 else 1)
        
        # Add some noise
        noise_level = 0.05
        ecg += np.random.normal(0, noise_level, len(t))
        
        # Plot the ECG
        plt.plot(t, ecg)
        plt.title(f'ECG - Heart Rate: {heart_rate} BPM')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude (mV)')
        plt.grid(True)
        
        # Add abnormality note if present
        if abnormal:
            plt.figtext(0.5, 0.01, f'Abnormal ECG - {abnormality_type.replace("_", " ").title()}', 
                        ha='center', fontsize=10, bbox={"facecolor":"red", "alpha":0.2, "pad":5})
        
        # Save the figure
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    @staticmethod
    def generate_chest_xray(patient_id: str, condition: Optional[str] = None) -> str:
        """
        Generate a simulated chest X-ray image.
        
        Args:
            patient_id: Patient ID to include in filename
            condition: Optional condition to simulate (pneumonia, etc.)
            
        Returns:
            Path to generated image file
        """
        # Ensure directory exists
        image_dir = os.path.join('data', 'images')
        ImageGenerator.ensure_dir(image_dir)
        
        # Create a unique filename
        import time
        timestamp = int(time.time())
        filename = f"xray_{patient_id}_{timestamp}.png"
        filepath = os.path.join(image_dir, filename)
        
        # Set up the plot
        plt.figure(figsize=(8, 10))
        
        # Create a simulated X-ray
        # Size of the image
        width, height = 800, 1000
        
        # Create empty image with gradient background (darker in the middle, lighter at edges)
        x, y = np.meshgrid(np.linspace(-1, 1, width), np.linspace(-1, 1, height))
        d = np.sqrt(x*x + y*y)
        background = 0.8 - 0.5 * np.exp(-0.5*d**2)
        
        # Add ribcage structure (simplified)
        image = background.copy()
        
        # Add lungs (two ellipses)
        for i in range(height):
            for j in range(width):
                # Normalize to [-1, 1]
                x = 2 * j / width - 1
                y = 2 * i / height - 1
                
                # Left lung
                left_lung = ((x + 0.35)**2 / 0.05 + (y - 0.1)**2 / 0.2) < 1
                
                # Right lung
                right_lung = ((x - 0.35)**2 / 0.05 + (y - 0.1)**2 / 0.2) < 1
                
                # Make lungs lighter
                if left_lung or right_lung:
                    image[i, j] += 0.2
        
        # Add spine
        for i in range(height):
            center = width // 2
            width_spine = 30
            if i > height // 3 and i < height * 2 // 3:
                for j in range(center - width_spine, center + width_spine):
                    if 0 <= j < width:
                        # Make spine darker
                        image[i, j] -= 0.2
        
        # Add condition-specific features
        if condition:
            condition = condition.lower()
            
            if 'pneumonia' in condition:
                # Add opacity in one lung (pneumonia infiltrate)
                side = random.choice(['left', 'right'])
                opacity_x = -0.35 if side == 'left' else 0.35
                opacity_y = random.uniform(-0.2, 0.3)
                opacity_size = random.uniform(0.05, 0.1)
                
                for i in range(height):
                    for j in range(width):
                        x = 2 * j / width - 1
                        y = 2 * i / height - 1
                        d = np.sqrt((x - opacity_x)**2 + (y - opacity_y)**2)
                        if d < opacity_size:
                            # Darken the area to simulate infiltrate
                            image[i, j] -= 0.3 * (1 - d/opacity_size)
                
                condition_text = f"Possible infiltrate in {side} lung"
            
            elif 'fracture' in condition or 'break' in condition:
                # Add rib fracture
                rib_y = random.uniform(-0.3, 0.3)
                rib_x = random.choice([-0.6, 0.6])  # Left or right side
                rib_length = random.uniform(0.1, 0.2)
                rib_angle = random.uniform(-30, 30)
                
                # Convert angle to radians
                angle_rad = rib_angle * np.pi / 180
                
                # Calculate end points
                x1 = rib_x - 0.5 * rib_length * np.cos(angle_rad)
                y1 = rib_y - 0.5 * rib_length * np.sin(angle_rad)
                x2 = rib_x + 0.5 * rib_length * np.cos(angle_rad)
                y2 = rib_y + 0.5 * rib_length * np.sin(angle_rad)
                
                # Draw the rib
                for i in range(height):
                    for j in range(width):
                        x = 2 * j / width - 1
                        y = 2 * i / height - 1
                        
                        # Calculate distance to the line segment
                        # (simplified for demonstration)
                        d = np.abs((y2-y1)*x - (x2-x1)*y + x2*y1 - y2*x1) / np.sqrt((y2-y1)**2 + (x2-x1)**2)
                        
                        if d < 0.02:
                            # Darken to simulate rib
                            image[i, j] -= 0.3
                
                # Add fracture point
                fracture_t = random.uniform(0.3, 0.7)  # Position along the rib
                fracture_x = x1 + fracture_t * (x2 - x1)
                fracture_y = y1 + fracture_t * (y2 - y1)
                
                # Draw fracture gap
                for i in range(height):
                    for j in range(width):
                        x = 2 * j / width - 1
                        y = 2 * i / height - 1
                        d = np.sqrt((x - fracture_x)**2 + (y - fracture_y)**2)
                        if d < 0.02:
                            # Make fracture gap lighter
                            image[i, j] += 0.5
                
                condition_text = "Possible rib fracture"
            
            elif 'cardiomegaly' in condition:
                # Enlarged heart (cardiomegaly)
                heart_x = 0
                heart_y = 0
                heart_size = random.uniform(0.25, 0.35)  # Enlarged
                
                for i in range(height):
                    for j in range(width):
                        x = 2 * j / width - 1
                        y = 2 * i / height - 1
                        d = np.sqrt((x - heart_x)**2 + (y - heart_y)**2)
                        if d < heart_size:
                            # Darken to simulate enlarged heart
                            image[i, j] -= 0.2 * (1 - d/heart_size)
                
                condition_text = "Possible cardiomegaly (enlarged heart)"
            
            else:
                # Generic abnormality
                abnormal_x = random.uniform(-0.5, 0.5)
                abnormal_y = random.uniform(-0.3, 0.3)
                abnormal_size = random.uniform(0.05, 0.15)
                
                for i in range(height):
                    for j in range(width):
                        x = 2 * j / width - 1
                        y = 2 * i / height - 1
                        d = np.sqrt((x - abnormal_x)**2 + (y - abnormal_y)**2)
                        if d < abnormal_size:
                            # Create a density
                            image[i, j] -= 0.3 * (1 - d/abnormal_size)
                
                condition_text = "Possible abnormality detected"
        else:
            condition_text = "No significant findings"
        
        # Plot the X-ray
        plt.imshow(image, cmap='gray')
        plt.title('Chest X-Ray')
        plt.axis('off')
        
        # Add condition note
        plt.figtext(0.5, 0.01, condition_text, 
                    ha='center', fontsize=10, 
                    bbox={"facecolor":"yellow" if condition else "green", 
                          "alpha":0.2, "pad":5})
        
        # Save the figure
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    @staticmethod
    def generate_blood_test_results(patient_id: str, condition: Optional[str] = None) -> Dict:
        """
        Generate simulated blood test results.
        
        Args:
            patient_id: Patient ID
            condition: Optional condition to simulate
            
        Returns:
            Dictionary with blood test results
        """
        # Define normal ranges for common blood tests
        normal_ranges = {
            'WBC': (4.5, 11.0, 'x10^9/L'),  # White blood cells
            'RBC': (4.2, 5.8, 'x10^12/L'),  # Red blood cells
            'Hemoglobin': (13.5, 17.5, 'g/dL'),  # Hemoglobin
            'Hematocrit': (41, 50, '%'),  # Hematocrit
            'Platelets': (150, 400, 'x10^9/L'),  # Platelets
            'Glucose': (70, 100, 'mg/dL'),  # Glucose
            'Sodium': (135, 145, 'mmol/L'),  # Sodium
            'Potassium': (3.5, 5.0, 'mmol/L'),  # Potassium
            'Chloride': (98, 107, 'mmol/L'),  # Chloride
            'Bicarbonate': (22, 29, 'mmol/L'),  # Bicarbonate
            'BUN': (8, 20, 'mg/dL'),  # Blood urea nitrogen
            'Creatinine': (0.6, 1.2, 'mg/dL'),  # Creatinine
            'Calcium': (8.5, 10.5, 'mg/dL'),  # Calcium
            'Phosphorus': (2.5, 4.5, 'mg/dL'),  # Phosphorus
            'Magnesium': (1.7, 2.2, 'mg/dL'),  # Magnesium
            'ALT': (7, 56, 'U/L'),  # Alanine aminotransferase
            'AST': (10, 40, 'U/L'),  # Aspartate aminotransferase
            'Troponin I': (0.0, 0.4, 'ng/mL'),  # Cardiac troponin I
            'CRP': (0, 3, 'mg/L'),  # C-reactive protein
        }
        
        # Generate normal results with random variation
        results = {}
        for test, (min_val, max_val, unit) in normal_ranges.items():
            # Normal distribution within range
            mean = (min_val + max_val) / 2
            std = (max_val - min_val) / 6  # 3 sigma = 99.7%
            results[test] = {
                'value': round(random.normalvariate(mean, std), 1),
                'unit': unit,
                'reference_range': f"{min_val}-{max_val}"
            }
        
        # Modify based on condition
        if condition:
            condition = condition.lower()
            
            if 'infection' in condition or 'pneumonia' in condition:
                # Elevated WBC, CRP in infections
                results['WBC']['value'] = round(random.uniform(11.1, 20.0), 1)
                results['CRP']['value'] = round(random.uniform(5, 100), 1)
            
            elif 'anemia' in condition:
                # Low hemoglobin, RBC in anemia
                results['Hemoglobin']['value'] = round(random.uniform(8.0, 13.0), 1)
                results['RBC']['value'] = round(random.uniform(3.0, 4.1), 1)
                results['Hematocrit']['value'] = round(random.uniform(30, 40), 1)
            
            elif 'dehydration' in condition:
                # Elevated sodium, BUN in dehydration
                results['Sodium']['value'] = round(random.uniform(146, 155), 1)
                results['BUN']['value'] = round(random.uniform(21, 30), 1)
                results['Creatinine']['value'] = round(random.uniform(1.3, 2.0), 1)
            
            elif 'diabetes' in condition:
                # Elevated glucose in diabetes
                results['Glucose']['value'] = round(random.uniform(120, 300), 1)
            
            elif 'liver' in condition:
                # Elevated liver enzymes in liver disease
                results['ALT']['value'] = round(random.uniform(60, 300), 1)
                results['AST']['value'] = round(random.uniform(45, 200), 1)
            
            elif 'cardiac' in condition or 'infarction' in condition or 'heart attack' in condition:
                # Elevated troponin in cardiac events
                results['Troponin I']['value'] = round(random.uniform(0.5, 10.0), 2)
            
            elif 'kidney' in condition or 'renal' in condition:
                # Elevated creatinine, BUN in kidney disease
                results['Creatinine']['value'] = round(random.uniform(1.3, 4.0), 1)
                results['BUN']['value'] = round(random.uniform(21, 60), 1)
                results['Potassium']['value'] = round(random.uniform(5.1, 6.5), 1)
            
            elif 'bleeding' in condition or 'hemorrhage' in condition:
                # Low hemoglobin, platelets in bleeding
                results['Hemoglobin']['value'] = round(random.uniform(8.0, 13.0), 1)
                results['Platelets']['value'] = round(random.uniform(50, 140), 1)
        
        # Mark abnormal values
        for test in results:
            min_val, max_val, _ = normal_ranges[test]
            value = results[test]['value']
            if value < min_val or value > max_val:
                results[test]['abnormal'] = True
                if value < min_val:
                    results[test]['direction'] = 'low'
                else:
                    results[test]['direction'] = 'high'
            else:
                results[test]['abnormal'] = False
        
        # Add patient info
        results['patient_id'] = patient_id
        results['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return results
    
    @staticmethod
    def get_normal_imaging_findings() -> List[str]:
        """Return a list of normal imaging findings descriptions."""
        return [
            "No significant abnormalities detected.",
            "Findings within normal limits.",
            "Normal anatomy visualized without evidence of disease.",
            "No acute findings.",
            "Normal examination with no pathological findings.",
            "Examination reveals no evidence of acute process.",
            "Normal study with no significant pathology identified."
        ]
    
    @staticmethod
    def get_abnormal_imaging_findings(condition: str) -> List[str]:
        """Return a list of abnormal imaging findings based on condition."""
        condition = condition.lower()
        
        if 'pneumonia' in condition:
            return [
                "Opacity in the right lower lobe consistent with pneumonia.",
                "Left upper lobe infiltrate suggesting pneumonic process.",
                "Bilateral patchy infiltrates consistent with pneumonia.",
                "Consolidation in the right middle lobe suggestive of pneumonia.",
                "Focal area of increased density in left lower lobe, consistent with pneumonic infiltrate."
            ]
        elif 'fracture' in condition:
            return [
                "Fracture of the 7th rib on the right side.",
                "Acute fracture of the left 5th rib without displacement.",
                "Minimally displaced fracture of the right 8th rib.",
                "Multiple rib fractures on the left side (ribs 4-6).",
                "Healing fracture of the right 9th rib with callus formation."
            ]
        elif 'cardiac' in condition or 'heart' in condition:
            return [
                "Cardiomegaly with cardiothoracic ratio of 0.65.",
                "Enlarged cardiac silhouette suggesting cardiomegaly.",
                "Mild pulmonary vascular congestion suggesting heart failure.",
                "Perihilar haziness consistent with pulmonary edema.",
                "Bilateral pleural effusions, likely due to heart failure."
            ]
        else:
            return [
                "Abnormal finding in the right upper quadrant.",
                "Radiographic abnormality requiring clinical correlation.",
                "Suspicious lesion detected, further evaluation recommended.",
                "Unexpected finding that warrants additional investigation.",
                "Patchy opacity of uncertain etiology, follow-up imaging suggested."
            ]


# For testing purposes
if __name__ == "__main__":
    # Test ECG generation
    ecg_path = ImageGenerator.generate_ecg("test001", 80, abnormal=True)
    print(f"ECG generated at: {ecg_path}")
    
    # Test X-ray generation
    xray_path = ImageGenerator.generate_chest_xray("test001", condition="pneumonia")
    print(f"X-ray generated at: {xray_path}")
    
    # Test blood test results
    blood_results = ImageGenerator.generate_blood_test_results("test001", condition="infection")
    print("Blood test results:", blood_results)
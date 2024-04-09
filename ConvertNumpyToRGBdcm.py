import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pydicom
import os
import pydicom.uid
import tkinter as tk
from tkinter import filedialog


rbc_array_path = None
bar_array_path = None
gas_array_path = None
rbc_description = None
bar_description = None
gas_description = None
Subject_name=None

###### GUI

def select_array(label):
    filename = filedialog.askopenfilename()
    if filename:
        label.config(text=filename)

def submit():
    global rbc_array_path, bar_array_path, gas_array_path, rbc_description, bar_description, gas_description,Subject_name
    rbc_array_path = label1.cget("text")
    rbc_description = entry2.get()
    bar_array_path = label3.cget("text")
    bar_description = entry4.get()
    gas_array_path = label5.cget("text")
    gas_description = entry6.get()
    Subject_name = entry7.get()
    
    print("RBC2gasRGB Array:", rbc_array_path)
    print("RBC2gasRGB Description:", rbc_description)
    print("Bar2gasRGB Array:", bar_array_path)
    print("Bar2gasRGB Description:", bar_description)
    print("Gas Array:", gas_array_path)
    print("Gas Description:", gas_description)
    print("Subject Name:", Subject_name)

    root.destroy()

root = tk.Tk()
root.title("User Input")

# Frame 1: RBC2gasRGB
frame1 = tk.Frame(root)
frame1.grid(row=0, column=0, padx=10, pady=5)
label1 = tk.Label(frame1, text="Select numpy array for RBC2gasRGB:")
label1.grid(row=0, column=0)
button1 = tk.Button(frame1, text="Browse", command=lambda: select_array(label1))
button1.grid(row=0, column=1)

# Frame 2: Series Description for RBC2gasRGB
frame2 = tk.Frame(root)
frame2.grid(row=0, column=2, padx=10, pady=5)
label2 = tk.Label(frame2, text="Write series description:")
label2.grid(row=0, column=0)
entry2 = tk.Entry(frame2)
entry2.grid(row=0, column=1)

# Frame 3: Bar2gasRGB
frame3 = tk.Frame(root)
frame3.grid(row=1, column=0, padx=10, pady=5)
label3 = tk.Label(frame3, text="Select numpy array for Bar2gasRGB:")
label3.grid(row=0, column=0)
button3 = tk.Button(frame3, text="Browse", command=lambda: select_array(label3))
button3.grid(row=0, column=1)

# Frame 4: Series Description for Bar2gasRGB
frame4 = tk.Frame(root)
frame4.grid(row=1, column=2, padx=10, pady=5)
label4 = tk.Label(frame4, text="Write series description:")
label4.grid(row=0, column=0)
entry4 = tk.Entry(frame4)
entry4.grid(row=0, column=1)

# Frame 5: Gas
frame5 = tk.Frame(root)
frame5.grid(row=2, column=0, padx=10, pady=5)
label5 = tk.Label(frame5, text="Select numpy array for Gas:")
label5.grid(row=0, column=0)
button5 = tk.Button(frame5, text="Browse", command=lambda: select_array(label5))
button5.grid(row=0, column=1)

# Frame 6: Series Description for Gas
frame6 = tk.Frame(root)
frame6.grid(row=2, column=2, padx=10, pady=5)
label6 = tk.Label(frame6, text="Write series description:")
label6.grid(row=0, column=0)
entry6 = tk.Entry(frame6)
entry6.grid(row=0, column=1)

# Frame 7: Subject Name
frame7 = tk.Frame(root)
frame7.grid(row=3, column=0, padx=10, pady=5)
label7 = tk.Label(frame7, text="Subject Name:")
label7.grid(row=0, column=0)
entry7 = tk.Entry(frame7)
entry7.grid(row=0, column=1)

# Submit Button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=4, columnspan=3, pady=10)

root.mainloop()


#####################   funcitons   #####################
def create_padded_matrix(colormap, desired_rows=128):
    colormap_array = np.array(colormap.colors)[::-1]

    each_col_row = 10
    each_col_col = 10

    vertical_colormap = colormap_array[:, np.newaxis, :]
    colorbar_matrix = np.repeat(vertical_colormap, each_col_col, axis=1)

    colbar_image = np.zeros(((colormap_array.shape[0]) * each_col_row, each_col_col, 3))
    for i in range(0, colbar_image.shape[2]):
        colbar_image[:, :, i] = np.repeat(colorbar_matrix[:, :, i], each_col_row, axis=0)

    padded_matrix = np.zeros((desired_rows, colbar_image.shape[1], colbar_image.shape[2]))
    start_index = (desired_rows - colbar_image.shape[0]) // 2
    padded_matrix[start_index:start_index + colbar_image.shape[0], :, :] = colbar_image

    return padded_matrix

colormap_bar2gas = ListedColormap([
    [1, 0, 0],            # Red
    [1, 0.7143, 0],       # Yellow
    [0.4, 0.7, 0.4],      # Green
    [0, 1, 0],            # Green
    [184.0/255.0, 226.0/255.0, 145.0/255.0],  # Custom color 1
    [243.0/255.0, 205.0/255.0, 213.0/255.0],  # Custom color 2
    [225.0/255.0, 129.0/255.0, 162.0/255.0],  # Custom color 3
    [197.0/255.0, 27.0/255.0, 125.0/255.0]    # Custom color 4
])

colormap_rbc2gas = ListedColormap([
        [0, 0, 0],
        [1, 0, 0],
        [1, 0.7143, 0],
        [0.4, 0.7, 0.4],
        [0, 1, 0],
        [0, 0.57, 0.71],
        [0, 0, 1]
])

colormap_gas = ListedColormap([
        [0, 0, 0],
        [1, 0, 0],
        [1, 0.7143, 0],
        [0.4, 0.7, 0.4],
        [0, 1, 0],
        [0, 0.57, 0.71],
        [0, 0, 1]
])
    
#############   Code Starts Here ##################


def create_dicoms_for_DP(data, colorbar, description,output_dir=None):
    if colorbar == 'RBC2Gas':
        sel_colorbar = colormap_rbc2gas
    elif colorbar == 'Bar2Gas':
        sel_colorbar = colormap_bar2gas
    elif colorbar == 'Gas':
        sel_colorbar = colormap_gas
    else:
        pass 
    colorbar_matrix = create_padded_matrix(sel_colorbar)
    concatenated_image = np.concatenate((data[:,:,1,:], colorbar_matrix), axis=1)
    rgb_image = np.zeros((concatenated_image.shape[0], concatenated_image.shape[1], data.shape[2], concatenated_image.shape[2]))

    for i in range(0, rgb_image.shape[2]):
        rgb_image[:,:,i,] = np.concatenate((data[:,:,i,:], colorbar_matrix), axis=1)

    ds = pydicom.dcmread('header_info.dcm')
    if output_dir is None:
        output_dir = colorbar
        ds.PatientName="XXXX"
        ds.SeriesDescription = f"{colorbar}_{description}"
    else:
        output_dir =  f"{colorbar}_{output_dir}" 
        ds.PatientName=f"{output_dir}" 
        ds.SeriesDescription = f"{colorbar}_{description}_{output_dir}"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    new_uid = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = new_uid

    num_dicoms = data.shape[2]
    all_locations = range(-64, 64, 1)
    num_bits = 8

    for i in range(num_dicoms):
        color_image = (rgb_image[:,:,i,:] * (2 ** num_bits - 1)).astype('uint%d' % num_bits)
        ds.PixelData = color_image.tobytes()
        ds.Rows, ds.Columns = color_image.shape[:2]
        ds.SamplesPerPixel = 3
        ds.PhotometricInterpretation = 'RGB'
        ds.BitsAllocated = num_bits
        ds.BitsStored = num_bits
        ds.InstanceNumber = i + 1
        ds.SliceLocation = all_locations[i]
        new_uid = pydicom.uid.generate_uid()
        ds.SOPInstanceUID = new_uid
        ds.NumberOfFrames = 1
        output_file = os.path.join(output_dir, f"dicom_{i}.dcm")
        ds.save_as(output_file)

############################

create_dicoms_for_DP(np.load(rbc_array_path), 'RBC2Gas', rbc_description,output_dir=Subject_name)
create_dicoms_for_DP(np.load(bar_array_path), 'Bar2Gas', bar_description,output_dir=Subject_name)
create_dicoms_for_DP(np.load(gas_array_path), 'Gas', gas_description,output_dir=Subject_name)

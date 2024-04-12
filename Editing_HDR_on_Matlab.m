clc; clear all; close all;

% Read in the DICOM image
dicom_info = dicominfo('Header_info.dcm');
dicom_image = dicomread(dicom_info);

dicom_info.StudyDate = 111111;
dicom_info.SeriesDate= 111111;
dicom_info.ContentDate=111111;
dicom_info.PatientBirthDate=111111;
dicom_info.PatientSex='X';
dicom_info.PatientAge='XYZ';
dicom_info.PatientSize=111;
dicom_info.PatientWeight=111;
dicom_info.MRAcquisitionType='3D';
dicom_info.SequenceName='XXX';
dicom_info.PulseSequenceName='XXX';


new_filename = 'Edited_Dicom_Header.dcm';
dicomwrite(dicom_image,new_filename,dicom_info,"CreateMode","Copy","MultiframeSingleFile",true);



import PySimpleGUI as sg
import os
from PyPDF2 import PdfFileMerger

sg.change_look_and_feel('DarkAmber')	# Add a touch of color
# All the stuff inside your window.
pdf_list = []
layout = [
	[sg.Text('PDFs')],
	[sg.Listbox(values=pdf_list, size=(60, 10), key='_list_', select_mode='SINGLE')],
	[sg.Text('Controls'), sg.Button(button_text='Move Up', key='Up'), sg.Button(button_text='Move Down', key='Down'), sg.Button(button_text='Remove', key='Remove'), sg.Button(button_text='Clear All', key='Clear')],
	[sg.InputText(), sg.FileBrowse(file_types=(("PDFs", "*.pdf"),), button_text='Browse', key='File'), sg.Button(button_text='Add', key='Add')],
	[sg.Button(button_text='Merge', key='Merge'), sg.Cancel()]
]

# Create the Window
window = sg.Window('Merge PDFs', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	if event in (None, 'Cancel'):   # if user closes window or clicks cancel
		break
	listbox = window['_list_']
	index = listbox.get_indexes()[0] if len(listbox.get_indexes()) > 0 else None
	if event == 'Add' and values['File'] != '':
		pdf_list.append(values['File'])
		index = len(pdf_list) - 1
	elif event =='Clear':
		pdf_list = []
	elif event == 'Merge':
		if len(pdf_list) == 0:
			sg.Popup('No PDFs to merge', title='Warning')
		else:
			merger = PdfFileMerger()
			for value in pdf_list:
				merger.append(value)
			# set path to desktop
			desktop_path = os.path.join(os.environ['HOMEPATH'], 'Desktop')
			output_path = os.path.join(desktop_path, 'merged.pdf')
			# set unique output file name
			counter = 0
			while os.path.exists(output_path):
				counter += 1
				output_path = os.path.join(desktop_path, f'merged{counter}.pdf')
			merger.write(output_path)
			sg.Popup('File successfully merged\n', 'Location: ', output_path)
	elif index is None:
		pass # do nothing
	elif event == 'Up':
		if index > 0:
			pdf_list[index], pdf_list[index-1] = pdf_list[index-1], pdf_list[index]
			index -= 1
	elif event == 'Down':
		if index < len(pdf_list)-1:
			pdf_list[index], pdf_list[index+1] = pdf_list[index+1], pdf_list[index]
			index += 1
	elif event == 'Remove':
		pdf_list.pop(index)
		index = None
	listbox.update(values=pdf_list, set_to_index=index, scroll_to_index=index)

window.close()

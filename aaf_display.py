from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy
import aaf2


class MainWindow(QWidget):
	def __init__(self, app):
		super().__init__()
		self.app = app
		self.setWindowTitle("AAF Display")

		# Create text input section
		h_layout_1 = QHBoxLayout()
		label = QLabel("Enter file name: ")
		self.line_edit = QLineEdit()
		button = QPushButton("Create")

		self.line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		button.clicked.connect(self.create_aaf_file)

		h_layout_1.addWidget(label)
		h_layout_1.addWidget(self.line_edit)
		h_layout_1.addWidget(button)

		# Create label text display
		h_layout_2 = QHBoxLayout()
		self.aaf_display = QLabel()
		h_layout_2.addWidget(self.aaf_display)

		# Load AAF file
		self.load_aaf_file("sample_data/simple.aaf")

		# Update main layout
		v_layout = QVBoxLayout()
		v_layout.addLayout(h_layout_1)
		v_layout.addLayout(h_layout_2)
		self.setLayout(v_layout)

	def quit_app(self):
		self.app.quit()

	def load_aaf_file(self, file_name):
		with aaf2.open(file_name, "r") as f:
			# Get the main composition
			main_comp = next(f.content.toplevel())

			text = "Name: " + str(main_comp.name) + "\n"
			text += "Created Time: " + str(main_comp['CreationTime'].value) + "\n\n"

			# Video, audio and other track types are stored in slots on a mob object
			text += "Segments" + "\n"
			for slot in main_comp.slots:
				segment = slot.segment
				text += str(segment) + "\n"

			# Update GUI to show file information
			self.aaf_display.setText(text)

	def create_aaf_file(self):
		new_file_location = "created_files/" + self.line_edit.text() + ".aaf"
		print("New files name: ", new_file_location)

		with aaf2.open(new_file_location, "w") as f:
			# Objects are created with a factory on the AAFFile object
			mob = f.create.MasterMob("Demo2")

			# Add the mob to the file
			f.content.mobs.append(mob)

			edit_rate = 25

			# Create a tape, so we can add timecode (optional)
			tape_mob = f.create.SourceMob()
			f.content.mobs.append(tape_mob)

			timecode_rate = 25
			start_time = timecode_rate * 60 * 60  # 1 hour
			tape_name = self.line_edit.text()

			# Add tape slots to tape mob
			tape_mob.create_tape_slots(tape_name, edit_rate, timecode_rate, media_kind="picture")

			# Create sourceclip that references timecode
			tape_clip = tape_mob.create_source_clip(1, start_time)

			# Import the generated media
			mob.import_dnxhd_essence("assets/sample.dnxhd", edit_rate, tape_clip)
			mob.import_audio_essence("assets/sample.wav", edit_rate)

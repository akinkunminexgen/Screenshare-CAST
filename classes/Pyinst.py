import subprocess
import os
import shutil

#getting the parent folder
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class PyToExeConverter:
    def __init__(self, script_path):
        self.script_path = f'{parent_dir}/storage/scripting/{script_path}'
        self.script_app = f'{parent_dir}/storage/scriptingexe/esharexe22.exe'
        self.fille = script_path
        self.message = ""

    def convert(self, one_file=True, console=True, output_dir=f'{parent_dir}/storage/scriptingexe'):
        """
        Convert the Python script to a .exe file.

        :param one_file: If True, generate a single .exe file.
        :param console: If True, keep the console window.
        :param output_dir: The directory where the .exe file will be saved.
        :return: The path to the generated .exe file.
        """
        if not os.path.isfile(self.script_path):
            raise FileNotFoundError(f"The script {self.script_path} does not exist.")
        
        if os.path.isfile(self.script_app):
            os.remove(self.script_app)
        
        options = []

        if one_file:
            options.append('--onefile')

        if not console:
            options.append('--noconsole')

        # Specify the output directory
        options.extend(['--distpath', output_dir])

        command = ['pyinstaller', *options, self.script_path]
        
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            self.message = "Error during conversion"
            print('Eroor ooooooooooo')
            print(result.stdout)
            print(result.stderr)
            raise Exception("Failed to convert the script to .exe")

        exe_name = os.path.splitext(os.path.basename(self.script_path))[0] + '.exe'
        exe_path = os.path.join(output_dir, exe_name)

        if not os.path.isfile(exe_path):
            raise FileNotFoundError(f"The executable {exe_path} was not created.")
        
        print(f"Successfully created {exe_path}")
        try:
            filename, file_extension = os.path.splitext(self.fille)
            os.remove(f"{parent_dir}/{filename}.spec")
            shutil.rmtree(f"{parent_dir}/build")
            print(f"File {filename}{file_extension} has been deleted successfully.")
        except Exception:
            print(f"An error has occurred!")
        return exe_path

# Example usage:
#converter = PyToExeConverter('anims.py')
#exe_path = converter.convert(one_file=True, console=True)
#print(f"Executable created at: {exe_path}")

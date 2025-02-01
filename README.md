# Blocks-Creator-1.0 [1.21.1]
 This project provides a Python utility that automatically generates JSON files and copies asset images for new Minecraft blocks, while also updating the Java mod source code with the new block names.

This project provides a comprehensive toolchain for Minecraft mod development targeting version 1.21.1. It consists of two main components:

-Python Utility (mod_creator.py / mod_creator.exe)
-Java Mod Source (MDK-1.21-ModDevGradle-main)

The Python utility, originally written in mod_creator.py, is responsible for generating all the necessary resource files required to add a new block to your Minecraft mod. These include JSON files for recipes, blockstates, and models (both for blocks and items), as well as copying the corresponding texture files. Additionally, the tool automatically updates the ExampleMod.java file by inserting the new block names into a designated loop, ensuring that your mod registers these blocks properly.

For convenience, an executable version named mod_creator.exe is provided. This EXE is built from the Python script and can be created by anyone using the provided source code if preferred. Note: Some of the UI text (e.g., labels and error messages) is in Polish, so expect a mix of Polish and English in the tool’s interface.

How It Works
Generate Resource Files:
Run mod_creator.exe (or build it yourself from mod_creator.py) and choose the project directory of downloaded MDK. The MDK folder is named MDK-1.21-ModDevGradle-main and is available to download.

Specify New Block Names:
In the tool’s GUI, paste a list of new block names (one per line). These names must match the names of the corresponding texture files (which you also select via the tool). Please avoid the capital letters. The script will generate JSON files for:

Recipes: To define how the block is obtained (currently every added block can be crafted by using dirt in stonecutter).
Blockstates: For proper block model variants.
Block Models: Specifying the parent model and texture mapping.
Item Models: For rendering the block as an item.
Update Java Mod Source:
The Python script automatically updates the ExampleMod.java file in your MDK project by inserting new block identifiers into a loop (using Java’s List.of(...) construct). This allows the mod’s code to register both static and dynamically added blocks during runtime.

Build Your Mod:
After running the Mod_Creator utility, open your MDK-1.21-ModDevGradle-main project in your preferred IDE (we recommend IntelliJ IDEA). Finally, build the project using Gradle. This will compile your mod and package it into a JAR file that you can load into Minecraft.

Summary how to add new blocks:

Run the Creator:
Launch mod_creator.exe (or build it from mod_creator.py if you prefer to compile it yourself).

Specify Project Path:
In the utility, choose the path to your MDK-1.21-ModDevGradle-main folder.

Input Block Names & Assets:
Paste the names of the new blocks into the text area.
These block names must exactly correspond to the filenames of the textures you want to add.
Select the image files for the block textures.
Generate and Update:
The tool will automatically generate the required JSON resource files, copy the images to the correct folders, and update ExampleMod.java with the new block registration entries.

Compile Your Mod:
Open the MDK project in IntelliJ IDEA and build the project via Gradle. The result will be a mod JAR that includes your newly added blocks in MDK-1.21-ModDevGradle-main\build\libs.

Summary
This project streamlines the process of adding custom blocks to a Minecraft mod by automating resource file generation and Java code updates. Whether you use the provided mod_creator.exe or compile it from source, you’ll save time and reduce manual errors in mod development. Enjoy building your mod with ease!

Acknowledgments

Special thanks to the original MDK-1.21-ModDevGradle-main project provided by the NeoForge team. Their MDK, available at https://github.com/NeoForgeMDKs/MDK-1.21-ModDevGradle, has been instrumental in the development of this toolchain and mod integration workflow.

max = 3; // set the max value of the images here - either 65535 for uint16, or 4096 if uint12 mapped
min = -3;

setBatchMode(true);

cmdoptions = getArgument;
cmdoptionssplit = split(cmdoptions," ");
FilePrefix = cmdoptionssplit[0];
target_dir = cmdoptionssplit[1];

source_file = target_dir + FilePrefix;
print(source_file);
open(source_file);
run("Size...", "width=300 depth=80 constrain average interpolation=Bilinear");
       run("Gaussian Blur...", "sigma=2 stack");
       setMinAndMax(min, max);
	run("8-bit");
	saveAs("tiff", target_dir + "/" + FilePrefix + "GauSmooth.tiff");
	close();
run("Collect Garbage");

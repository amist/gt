=== First ===
--- How to run a test ---
Prepare data:
    Choose the dataset from here: http://www.math.uwaterloo.ca/tsp/data/
    Convert the data to my json format - replace the last point with '0'. Note the keys are strings.
    Save the data file in gt/examples folder.
    Make the order file. In gt/examples folder run:
        python create_order.py cities_file.json > order_file.json
Configuration:
    tsp_evolve.config:
        [runner]
        output_mode = console
        [population]
        type = SimplePopulation
        evolution_type = progressive
        [individual]
        class = gt.examples.tsp_evolve.TSPEvolve
        evolution_type = progressive
        chromosome_type = a
        [problem]
        (for example) data_file = gt/examples/vlsi131.json
        (for example) order_file = gt/examples/aaorder_vlsi131.json
Run:
    Don't need that anymore:
        Edit gt/tests/test_tsp_evolve.py:
            Choose the starting point.
    Run:
        python -m gt.tests.test_tsp_evolve
    Or (edit the file first for number of iterations):
        collect_data_evolve.bat
             
--- How to animate a test run ---
Each run creates a log in the logs folder, named according to the run's time.
In animate_log.py:
    Change log_files list according to the logs you want to animate.
From Anaconda prompt, run:
    python animate_log.py
Running animate_log.py creates for each log file a folder of images (an image for each generation) in log_animations folder. The name is the same as the original log file.
In log_animations/create_vid.bat:
    Change the log folder name
From log_animations, run:
    create_vid.bat
        
        
=== Second ===
--- How to run a test ---
Prepare data:
    Like in the first.
Configuration:
    tsp_partial_template.config:
        [runner]
        output_mode = console
        [population]
        type = SimplePopulation
        [individual]
        class = gt.examples.tsp_multiple.TSPMultiple
        evolution_type = simple
        generations_evolution_step = 10
        evolution_start = 0
        [problem]
        (for example) data_file = gt/examples/vlsi131.json
        (for example) order_file = gt/examples/aaorder_vlsi131.json
Run:
    Edit gt/tests/test_tsp_partial.py:
        In main(), edit the number of runs.
    Run:
        python -m gt.tests.test_tsp_partial
        
--- How to animate a test run ---
Each run creates a log in the logs folder, named according to the run's time.
In animate_log_multiple.py:
    Change log_files list according to the logs you want to animate.
From Anaconda prompt, run:
    python animate_log_multiple.py
Running animate_log_multiple.py creates folder of images (an image for each generation) in log_animations folder. The name is the same as the original log file.
In log_animations/create_vid.bat:
    Change the log folder name
From log_animations, run:
    create_vid.bat
    
from dspy.teleprompt.ensemble import Ensemble

# Initialize the Ensemble class
teleprompter = Ensemble(reduce_fn=my_reduce_fn, size=3, deterministic=False)

# Compile the ensemble of programs
compiled_program = teleprompter.compile(programs)

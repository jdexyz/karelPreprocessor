# karelPreprocessor

Fanuc's Karel robot programming language limits variable names length to 12 characters. This is annoying when writing long programs.

This small python script takes a `.kl` karel file as input and parses it.
The variable names are then shortened in a deterministic way via a hash function. The line numbers are also preserved.

## Usage 

In a terminal in the downloaded repo folder, type : 

```bash
python preprocessor.py -i INPUT_FILE.kl -o OUTPUT_FILE.kl
```

You can then use `ktrans.exe` on the output file to get your compiled `.pc` file.

## Disclaimer

Although used extensively during months on an actual Fanuc robot, this script could still create bugs in your Karel programs that could result in unexpected robot behaviour. Always check the generated code before loading it on an actual robot.
We offer no warranty regarding the validity of the generated code, and disclaim liability for any damages resulting from its use.

## License

MIT Licensed

## Contributing

It would be nice to add more advanced preprocessing, and even basic syntax checking, to make error messages more explicit than with `ktrans.exe`. 
I would also be more prudent to build a test suite.

Pull requests are welcomed !
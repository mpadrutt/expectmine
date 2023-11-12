# Troubleshooting

## Known issues

### Python version below 3.10
```console
TypeError: unsupported operand type(s) for |: 'type' and 'type'
```
Type unions using | (e.g. `str | bool`) where introduced in python 3.10. 
Make sure you use a python version >= 3.10.
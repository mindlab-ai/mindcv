- `modules` for unit test (UT): test the main modules including dataset, transform, loader, model, loss, optimizer, and scheduler.  

To test all modules: 
```shell
pytest test/modules/*.py
```

- `tasks` for system test (ST): test the training and validation pipeline. 

To test the training process (in graph mode and pynative+ms_function mode) and the validation process, run
```shell
pytest test/task/test_train_val.py
```



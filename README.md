# Myo DashBoard

A basic Dash application to explore EMG signals and test different cut-off frequencies for common butter-worth filters.

## Usage

```bash
python main.py
```

## Content

### How to use the Myo App

The Explore EMG signal page allows you to explore EMG signals and test different cut-off frequencies for common butter-worth filters..

#### Test the app

Two EMG example files have been provided in the `data` folder to test the App directly.
For the two files, acquisition frequency is 2000Hz

#### Import your own data

You can upload EMG files directly through the app.
Please see and adapt the `import_emg` function in the `pipeline.py` file to match your data format.
The app is expecting that the `import_emg` function returns a pandas.Dataframe with emg as columns and a
pandas.Series reprensenting the time array.

**Note:** The app may be slow to respond to large files. We should improve it by
splitting the update_graph function (see in exploreemg_content.py) into several functions to avoid
updating all graph and reloading data every time the callback is executed. We can also improve usability
by updating the data (e.g., changing cut-off frequencies) without rescaling the graph.

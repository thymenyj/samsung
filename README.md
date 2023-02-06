For this project we used the CRISP-DM model.
- Business Understanding
- Data Understanding
- Data Preparation
- Data Modelling
- Evaluation
- Deployment

The project is divided into two phases. In the first phase a jupyter server is used. This was easier for the inital understanding and analysis. In the second
phase I made the code more production ready by changing the architecture.

The jupyter architecture uses local data downloaded from kaggle manually. The jupyter server is runned in a docker container.

![image](https://user-images.githubusercontent.com/36238233/217044334-049a603b-959a-4458-b83d-78f7fb72510e.png)

The deployment architecture uses the and API (FastAPI) to handle all the programming logic. There are three endpoints: [1] loading and processing data from kaggle to 
a postgres database, [2] training a random forest model and saving it and [3] a prediction service which can predict whether an input (visitor) will generate revenue.

![image](https://user-images.githubusercontent.com/36238233/217044419-99dc2be3-8b3d-4794-bb69-147e99902869.png)


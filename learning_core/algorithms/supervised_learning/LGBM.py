import lightgbm as lgb
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

kfold = KFold(n_splits = 30, shuffle=True, random_state = 5)
parameters = {
    'num_leaves':250, 
    'objective':'binary',  
    'max_depth':2,
    'learning_rate':.05,
    'max_bin':100
}

class LGBMAlgorithm:
    lgbm = {};
    
    forecasters_base = [];
    target_base = [];
    
    x_training = [];
    y_training = [];
    x_test = [];
    y_test = [];
    
    predict_test = [];
    accuracy_test = 0.0;
    predict_training = [];
    accuracy_test = 0.0;
    
    average_cross_validation = 0.0;
    
    confusion_matrix_test = [];
    confusion_matrix_training = [];

    def learning(self, x_training, y_training):        
        self.x_training = x_training;
        self.y_training = y_training;
        
        dataset = lgb.Dataset(x_training,label=y_training);
        self.lgbm= lgb.train(parameters,dataset,num_boost_round=200)
        
    def predict(self, x_test, y_test=[], accuracy=True):
        self.x_test = x_test;
        self.y_test = y_test;

        self.predict_test = self.lgbm.predict(x_test);
        self.treatResponseTest();
        
        if(accuracy and len(y_test) > 0):
            self.accuracy_test = accuracy_score(y_test, self.predict_test) * 100.0;
        
        return self.predict_test;
         
    
    def validateAlgorithm(self, forecasters_base, target_base):
        self.forecasters_base = forecasters_base;
        self.target_base = target_base;
        
        self.predict_training = self.lgbm.predict(self.x_training);
        self.treatResponseTrainning();
        self.accuracy_training = accuracy_score(self.y_training, self.predict_training) * 100.0;
        
        self.confusion_matrix_test = confusion_matrix(self.y_test, self.predict_test);
        self.confusion_matrix_training = confusion_matrix(self.y_training, self.predict_training);
        
        model = lgb.LGBMClassifier(parameters);
        self.average_cross_validation = cross_val_score(model, forecasters_base, target_base, cv = kfold).mean() * 100.0;
        
        return {
            'accuracy_training': self.accuracy_training,
            'accuracy_test': self.accuracy_test,
            'average_cross_validation': self.average_cross_validation,
        }
        
    def treatResponseTest(self):
        for i in range(0, len(self.predict_test)):
            if self.predict_test[i] >= .5:       
                self.predict_test[i] = 1
            else:  
                self.predict_test[i] = 0
    
    def treatResponseTrainning(self):
        for i in range(0, len(self.predict_training)):
            if self.predict_training[i] >= .5:       
                self.predict_training[i] = 1
            else:  
                self.predict_training[i] = 0
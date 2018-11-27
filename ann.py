# load pima indians dataset
import numpy
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.optimizers import SGD


class Ann:
  def __init__(self, dataset: numpy):
    # split into input (X) and output (Y) variables
    X = dataset[:, 0:16]
    Y = dataset[:, 16:21]

    # create model
    model = Sequential()
    model.add(Dense(200, input_dim=16, activation='relu'))
    # model.add(Dense(8, activation='relu'))
    model.add(Dense(4, activation='softmax'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # model.add(Dense(64, activation='relu', input_dim=16))
    # model.add(Dropout(0.5))
    # model.add(Dense(64, activation='relu'))
    # model.add(Dropout(0.5))
    # model.add(Dense(64, activation='relu'))
    # model.add(Dropout(0.5))
    # model.add(Dense(4, activation='softmax'))
    #
    # sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
    # model.compile(loss='categorical_crossentropy',
    #   optimizer=sgd,
    #   metrics=['accuracy'])

    model.fit(X, Y, epochs=150, batch_size=10)
    # evaluate the model
    scores = model.evaluate(X, Y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    self.model = model

  def predict(self, X):
    predict = self.model.predict(X)

    maximum = max(predict[0])
    action = 0
    for i in range(0, 4):
      if predict[0][i] == maximum:
        action = i

    return action

  def fit(self, dataset, epochs):
    X = dataset[:, 0:16]
    Y = dataset[:, 16:21]
    self.model.fit(X, Y, epochs=150)
    scores = self.model.evaluate(X, Y)
    print("\n%s: %.2f%%" % (self.model.metrics_names[1], scores[1] * 100))

import matplotlib.pyplot as plt
import numpy as np



def main():
	# x = np.linspace(0, 2*np.pi, 200)
	# y = np.sin(x)

	# fig, ax = plt.subplots()
	# ax.plot(x, y)
	# plt.show()

 
	b = np.matrix([[1, 2], [3, 4]])
	b_asarray = np.asarray(b)

	np.random.seed(19680801)  # seed the random number generator.
	data = {'a': np.arange(50),
			'c': np.random.randint(0, 50, 50),
			'd': np.random.randn(50)}
	data['b'] = data['a'] + 10 * np.random.randn(50)
	data['d'] = np.abs(data['d']) * 100

	fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
	ax.scatter('a', 'b', c='c', s='d', data=data)
	ax.set_xlabel('entry a')
	ax.set_ylabel('entry b')

	x = np.linspace(0, 2, 100)  # Sample data.

	# Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
	fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
	ax.plot(x, x, label='linear')  # Plot some data on the axes.
	ax.plot(x, x**2, label='quadratic')  # Plot more data on the axes...
	ax.plot(x, x**3, label='cubic')  # ... and some more.
	ax.set_xlabel('x label')  # Add an x-label to the axes.
	ax.set_ylabel('y label')  # Add a y-label to the axes.
	ax.set_title("Simple Plot")  # Add a title to the axes.
	ax.legend();  # Add a legend.


if __name__ == "__main__":
	main()
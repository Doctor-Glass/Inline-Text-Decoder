import requests
import numpy
import sys
from bs4 import BeautifulSoup

url = "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub"

# Take in the page URL and parse it, returning an array with all of the coordinates and respective characters
def parse_page(url):
  # Get the page and store it
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  table = soup.find('table')
  x_coords = []
  y_coords = []
  characters = []

  # Pull all of the cells as individual elements
  for data in table.find_all('tr'):
    x_coords += data.find_all('span')[0]
    y_coords += data.find_all('span')[2]
    characters += data.find_all('span')[1]
  
  # Remove the header rows
  x_coords = x_coords[1:]
  y_coords = y_coords[1:]
  characters = characters[1:]

  # Compose the output
  output = numpy.array([x_coords, y_coords, characters])

  return output

# Take in a parsed bi-dimensional input array and return a bi-dimensional array of characters
def build_arrays(input):  
  # Get max X and Y values
  x_max = array_max(input[0])
  y_max = array_max(input[1])

  # Build our initial array array
  output = [[]] * (y_max + 1)

  # Build the empty arrays we need
  for i in range(0, y_max + 1):
    output[i] = [" "] * x_max

  # Add characters to their spots in the array
  for i in range(0, len(input[2])):
    x_index = int(input[0][i]) - 1
    y_index = int(input[1][i])

    output[y_index][x_index] = str(input[2][i])

  return output

# Take in an array and the value of the largest element within
def array_max(input):
  max = 0

  for item in input:
    if int(item) > max:
      max = int(item)

  return max

# Take in a bi-dimensional array and print each constituent array to the screen on a new line
def print_text(input):
  # Reverse the lists so the text is printed the right way up
  input = input [::-1]

  for i in range(len(input)):
    output = ""

    for j in range(len(input[i])):
      output += input[i][j]

    print(output)


  return False

def main():
  try:
    if sys.argv[1] != None:
      url = sys.argv[1]
  except:
    url = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"

  # Parse the page to get the raw data
  characterArray = parse_page(url)

  # Build output character arrays
  outputArray = build_arrays(characterArray)

  # Print the output
  print_text(outputArray)

if __name__ == '__main__':
  main()
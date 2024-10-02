import os

class Node:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.next = None  # points to the next node (element)


# sparse matrix class using a linked list to store non-zero elements.
class SparseMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.head = None  # start of the linked list for non-zero elements

    def insert(self, row, col, value):
        if value == 0:
            return
        new_node = Node(row, col, value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    @staticmethod
    def from_file(file_path):
        with open(file_path, 'r') as file:
            rows = int(file.readline().split('=')[1])
            cols = int(file.readline().split('=')[1])
            matrix = SparseMatrix(rows, cols)
            for line in file:
                row, col, value = eval(line.strip())
                matrix.insert(row, col, value)
        return matrix

    def __repr__(self):
        elements = []
        current = self.head
        while current:
            elements.append(f"({current.row}, {current.col}, {current.value})")
            current = current.next
        return '\n'.join(elements)

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")
            current = self.head
            while current:
                file.write(f"({current.row}, {current.col}, {current.value})\n")
                current = current.next

# function to add matrices
def add_matrices(matrix1, matrix2):
    result = SparseMatrix(matrix1.rows, matrix1.cols)
    current1 = matrix1.head
    current2 = matrix2.head

    while current1 or current2:
        if current1 and (not current2 or (current1.row, current1.col) < (current2.row, current2.col)):
            result.insert(current1.row, current1.col, current1.value)
            current1 = current1.next
        elif current2 and (not current1 or (current2.row, current2.col) < (current1.row, current1.col)):
            result.insert(current2.row, current2.col, current2.value)
            current2 = current2.next
        else:
            sum_value = current1.value + current2.value
            if sum_value != 0:
                result.insert(current1.row, current1.col, sum_value)
            current1 = current1.next
            current2 = current2.next
    return result

# function to subtract matrices
def subtract_matrices(matrix1, matrix2):
    result = SparseMatrix(matrix1.rows, matrix1.cols)
    current1 = matrix1.head
    current2 = matrix2.head

    while current1 or current2:
        if current1 and (not current2 or (current1.row, current1.col) < (current2.row, current2.col)):
            result.insert(current1.row, current1.col, current1.value)
            current1 = current1.next
        elif current2 and (not current1 or (current2.row, current2.col) < (current1.row, current1.col)):
            result.insert(current2.row, current2.col, -current2.value)
            current2 = current2.next
        else:
            diff_value = current1.value - current2.value
            if diff_value != 0:
                result.insert(current1.row, current1.col, diff_value)
            current1 = current1.next
            current2 = current2.next
    return result

# function to multiply matrices
def multiply_matrices(matrix1, matrix2):
    if matrix1.cols != matrix2.rows:
        raise ValueError("Matrix dimensions do not allow multiplication.")
    result = SparseMatrix(matrix1.rows, matrix2.cols)

    current1 = matrix1.head
    while current1:
        current2 = matrix2.head
        while current2:
            if current1.col == current2.row:
                result.insert(current1.row, current2.col, current1.value * current2.value)
            current2 = current2.next
        current1 = current1.next

    return result

# ask user for operation
def get_user_choice():
    print("\nSelect an operation to perform:")
    print("1. Add Matrices")
    print("2. Subtract Matrices")
    print("3. Multiply Matrices")
    return input("Enter your choice (1/2/3): ")

def main():
    # load matrices from files
    matrix1 = SparseMatrix.from_file('dsa_terry/sample_inputs/matrixfile1.txt')
    matrix2 = SparseMatrix.from_file('dsa_terry/sample_inputs/matrixfile3.txt')

    # process user's choice for matrix operation
    choice = get_user_choice()

    if choice == '1':
        result = add_matrices(matrix1, matrix2)
        print("\nResult of matrix addition:")
    elif choice == '2':
        result = subtract_matrices(matrix1, matrix2)
        print("\nResult of matrix subtraction:")
    elif choice == '3':
        result = multiply_matrices(matrix1, matrix2)
        print("\nResult of matrix multiplication:")
    else:
        print("Invalid choice!")
        return

    print(result)

    # ask user to save the result or not
    save = input("\nDo you want to save the result to a file? (yes/no): ").lower()
    if save == 'yes':
        output_folder = 'dsa_terry/sample_outputs'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_file = os.path.join(output_folder, 'result.txt')
        result.save_to_file(output_file)
        print(f"\nResult saved to {output_file}")
    else:
        print("\nResult not saved.")

if __name__ == '__main__':
    main()
# Reconciliation API

This is a Django + Django REST Framework backend for reconciling CSV financial data. It supports uploading a CSV file, identifying matches and mismatches, and exporting the result as either JSON or CSV.

---

## 🔧 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/reconciliation-assignment.git
cd reconciliation-assignment

2. **Create a virtual environment**

```bash
python -m venv venv
```
3. **Activate the virtual environment**
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```
4. **Install the required packages**

```bash
pip install -r requirements.txt
```
5. **Run the migrations**

```bash
python manage.py migrate
```
6. **Run the server**

```bash
python manage.py runserver
```
7. **Access the API**

    ***JSON***

    ```bash
    POST /api/reconcile
    ```

    ***CSV***

    ```bash
    POST /api/reconcile/?format=csv
    ```
    - Upload a CSV file with the same structure as the JSON payload.
    - The CSV file should have the following columns: `date`, `description`, `amount`, `type`.
    - The `type` column should be either `income` or `expense`.
    - The `amount` column should be a numeric value.
    - The `date` column should be in the format `YYYY-MM-DD`.
    - The `description` column can be any string.
    - The CSV file should be less than 5MB in size.

8. **Test the API**

    - You can use Postman or any other API testing tool to test the API.
    - The API supports both JSON and CSV formats.
    - The API returns a JSON response with the following structure:
        ```json
        {
            "matches": [
                {
                    "id": 1,
                    "date": "2023-01-01",
                    "description": "Salary",
                    "amount": 1000,
                    "type": "income"
                },
                ...
            ],
            "mismatches": [
                {
                    "id": 2,
                    "date": "2023-01-02",
                    "description": "Groceries",
                    "amount": 200,
                    "type": "expense"
                },
                ...
            ]
        }
        ```
    - The `matches` array contains all the transactions that match with the uploaded file.
    - The `mismatches` array contains all the transactions that do not match with the uploaded file.
    - The API also supports pagination for the `matches` and `mismatches` arrays.
    - The API supports filtering by date, description, amount, and type.
    - The API supports sorting by date, description, amount, and type.
    - The API supports searching by date, description, amount, and type.


## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
## 📧 Author
This project has been built by [Joy Kwamboka](https://github.com/kwambiee)








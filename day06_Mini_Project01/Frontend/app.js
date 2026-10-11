
/* ==========================================
   BOOKWORM — PERSONAL LIBRARY
   Frontend prototype
========================================== */

// 1. SAMPLE DATA
// Later, this data will come from our FastAPI backend.

let books = [];

let nextId = Math.max(0, ...books.map(book => book.id)) + 1;

// 2. DOM REFERENCES

const bookGrid = document.getElementById("book-grid");
const bookDialog = document.getElementById("book-dialog");
const bookForm = document.getElementById("book-form");
const searchInput = document.getElementById("search-input");
const statusFilter = document.getElementById("status-filter");
const formError = document.getElementById("form-error");

const bookIdInput = document.getElementById("book-id");
const titleInput = document.getElementById("book-title");
const authorInput = document.getElementById("book-author");
const yearInput = document.getElementById("book-year");
const bookStatusInput = document.getElementById("book-status");
// ========================================
async function loadBooks() {
    try {
        const response = await fetch("http://127.0.0.1:8000/books");

        if (!response.ok) {
            throw new Error("Failed to load books");
        }

        const data = await response.json();
        books = data.books;

        renderBooks();
    } catch (error) {
        console.error("Error loading books:", error);
    }
}

// 3. UPDATE LIBRARY COUNT

function updateLibraryCount() {
    const countElement = document.getElementById("library-count");

    if (countElement) {
        countElement.textContent = `(${books.length})`;
    }
}

// 4. CREATE BOOK COVER

function createBookCover(book) {
    const coverArea = document.createElement("div");
    coverArea.className = "book-cover";

    if (book.cover) {
        const image = document.createElement("img");

        image.src = book.cover;
        image.alt = `Cover of ${book.title}`;
        image.loading = "lazy";

        // If an image cannot load, display a title placeholder.
        image.addEventListener("error", () => {
            const placeholder = createCoverPlaceholder(book.title);
            coverArea.replaceChildren(placeholder);
        }, { once: true });

        coverArea.appendChild(image);
    } else {
        coverArea.appendChild(createCoverPlaceholder(book.title));
    }

    return coverArea;
}

function createCoverPlaceholder(titleText) {
    const placeholder = document.createElement("div");
    placeholder.className = "book-cover-placeholder";
    placeholder.textContent = titleText;
    return placeholder;
}

// 5. CREATE A BOOK CARD

function createBookCard(book) {
    const card = document.createElement("article");
    card.className = "book-card";

    // Cover
    const cover = createBookCover(book);

    // Details
    const details = document.createElement("div");
    details.className = "book-details";

    const title = document.createElement("h2");
    title.className = "book-title";
    title.textContent = book.title;
    title.title = book.title;

    const author = document.createElement("p");
    author.className = "book-author";
    author.textContent = book.author;

    const year = document.createElement("p");
    year.className = "book-year";
    year.textContent = String(book.year);

    const status = document.createElement("span");
    status.className =
        "book-status status-" +
        book.status.toLowerCase().replaceAll(" ", "-");
    status.textContent = book.status;

    details.append(title, author, year, status);

    // Actions
    const actions = document.createElement("div");
    actions.className = "book-actions";

    const editButton = document.createElement("button");
    editButton.type = "button";
    editButton.className = "edit-button";
    editButton.textContent = "Edit";
    editButton.setAttribute("aria-label", `Edit ${book.title}`);
    editButton.addEventListener("click", () => openEditDialog(book.id));

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "delete-button";
    deleteButton.textContent = "Delete";
    deleteButton.setAttribute("aria-label", `Delete ${book.title}`);
    deleteButton.addEventListener("click", () => deleteBook(book.id));

    actions.append(editButton, deleteButton);

    card.append(cover, details, actions);

    return card;
}

// 6. RENDER BOOKS WITH SEARCH AND FILTER

function renderBooks() {
    const searchTerm = searchInput.value.trim().toLowerCase();
    const selectedStatus = statusFilter.value;

    const filteredBooks = books.filter(book => {
        const matchesSearch =
            book.title.toLowerCase().includes(searchTerm) ||
            book.author.toLowerCase().includes(searchTerm);

        const matchesStatus =
            selectedStatus === "all" ||
            book.status === selectedStatus;

        return matchesSearch && matchesStatus;
    });

    bookGrid.replaceChildren();

    if (filteredBooks.length === 0) {
        const emptyMessage = document.createElement("p");
        emptyMessage.className = "empty-state";
        emptyMessage.textContent = books.length === 0
            ? "Your library is empty. Add your first book!"
            : "No books match your search or selected filter.";

        bookGrid.appendChild(emptyMessage);
    } else {
        filteredBooks.forEach(book => {
            bookGrid.appendChild(createBookCard(book));
        });
    }

    updateLibraryCount();
}

// 7. OPEN ADD BOOK DIALOG

function openAddDialog() {
    bookForm.reset();

    bookIdInput.value = "";
    document.getElementById("dialog-title").textContent = "Add New Book";
    document.getElementById("save-book-button").textContent = "Add Book";

    formError.textContent = "";

    bookDialog.showModal();
}

document.getElementById("add-book-button")
    .addEventListener("click", openAddDialog);

// 8. OPEN EDIT BOOK DIALOG

function openEditDialog(bookId) {
    const book = books.find(item => item.id === bookId);

    if (!book) return;

    bookIdInput.value = String(book.id);
    titleInput.value = book.title;
    authorInput.value = book.author;
    yearInput.value = String(book.year);
    bookStatusInput.value = book.status;

    document.getElementById("dialog-title").textContent = "Edit Book";
    document.getElementById("save-book-button").textContent = "Save Changes";

    formError.textContent = "";

    bookDialog.showModal();
}


 // 9. ADD OR UPDATE BOOK

bookForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    formError.textContent = "";

    const idValue = bookIdInput.value.trim();
    const title = titleInput.value.trim();
    const author = authorInput.value.trim();
    const year = Number(yearInput.value);
    const status = bookStatusInput.value;

    if (!title || !author) {
        formError.textContent = "Title and author are required.";
        return;
    }

    if (!Number.isInteger(year) || year < 1 || year > 2100) {
        formError.textContent = "Enter a valid publication year.";
        return;
    }

    if (!["Want to Read", "Reading", "Completed"].includes(status)) {
        formError.textContent = "Select a valid reading status.";
        return;
    }

    try {
        let url = "http://127.0.0.1:8000/books";
        let method = "POST";
        let cover = "";

        if (idValue) {
            const existingBook = books.find(
                item => item.id === Number(idValue)
            );

            if (!existingBook) {
                formError.textContent = "Book not found.";
                return;
            }

            cover = existingBook.cover || "";
            url = `${url}/${idValue}`;
            method = "PUT";
        }

        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title,
                author,
                year,
                status,
                cover
            })
        });

        if (!response.ok) {
            throw new Error("Failed to save book.");
        }

        await loadBooks();
        bookDialog.close();

    } catch (error) {
        console.error("Save book error:", error);
        formError.textContent =
            "Could not save the book. Please try again.";
    }
});


// 10. DELETE BOOK


async function deleteBook(bookId) {
    const book = books.find(item => item.id === bookId);

    if (!book) return;

    const confirmed = window.confirm(
        `Delete "${book.title}" from your library?`
    );

    if (!confirmed) return;

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/books/${bookId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error("Failed to delete book.");
        }

        await loadBooks();

    } catch (error) {
        console.error("Delete book error:", error);
        alert("Could not delete the book. Please try again.");
    }
}


// 11. CLOSE DIALOG

document.getElementById("close-dialog")
    .addEventListener("click", () => bookDialog.close());

document.getElementById("cancel-dialog")
    .addEventListener("click", () => bookDialog.close());

// 12. SEARCH AND FILTER

searchInput.addEventListener("input", renderBooks);
statusFilter.addEventListener("change", renderBooks);

// Prevent the search form from refreshing the page.
document.getElementById("search-form")
    .addEventListener("submit", event => {
        event.preventDefault();
        renderBooks();
    });

// 13. DARK MODE

const themeToggle = document.getElementById("theme-toggle");

themeToggle.addEventListener("click", () => {
    const isDark = document.body.classList.toggle("dark-theme");

    themeToggle.textContent = isDark ? "☀" : "♧";

    themeToggle.setAttribute(
        "aria-label",
        isDark ? "Switch to light mode" : "Switch to dark mode"
    );
});

// 14. INITIALIZE

renderBooks();
loadBooks();

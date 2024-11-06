// static/js/budgets.js

// Функция для подтверждения удаления
function confirmDelete() {
    return confirm("Вы уверены, что хотите удалить этот элемент?");
}

// Применяем функцию подтверждения удаления ко всем кнопкам с классом 'btn-danger'
document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.btn-danger');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            if (!confirmDelete()) {
                event.preventDefault(); // Отменяем действие, если пользователь не подтвердил
            }
        });
    });
});

window.onload = function() {
        var gradeFilter = document.getElementById('gradeFilter');
        var radios = document.querySelectorAll('input[type="radio"]');

        gradeFilter.addEventListener('change', filterByGrade);

        radios.forEach(radio => {
            radio.addEventListener('change', filterByGrade);
        });

    function filterByGrade() {
        var selected_grade = gradeFilter.value;

        const selectedRadio = document.querySelector('input[type="radio"]:checked');
        var rows= document.getElementsByClassName('student');

        if(selectedRadio.value === '未繳費'){
            for (var i = rows.length - 1; i >= 0; i--) {
                rows[i].classList.remove('not');
                var payment_or_not = rows[i].getElementsByClassName('payment')[0];
                payment_or_not= payment_or_not.getElementsByTagName('span')[0];

                if(payment_or_not.classList.contains('sudah')){
                    rows[i].classList.add('not');
                }
            }
        }else if(selectedRadio.value === '已繳費'){
            for (var i = rows.length - 1; i >= 0; i--) {
                rows[i].classList.remove('not');
                var payment_or_not = rows[i].getElementsByClassName('payment')[0];
                payment_or_not= payment_or_not.getElementsByTagName('span')[0];

                if(payment_or_not.classList.contains('belum')){
                    rows[i].classList.add('not');
                    // console.log(payment_or_not)
                }
            }
        }else{
             for (var i = rows.length - 1; i >= 0; i--) {
                rows[i].classList.remove('not');
            }
        }

        for (var i = 0; i < rows.length; i++) {
            if (rows[i].classList.contains('not')) {
                rows[i].style.display = 'none';
            }else{
                rows[i].style.display = 'table-row';
                var grade = rows[i].getElementsByClassName('years_old')[0].innerText.trim();

                if (selected_grade === 'all' || grade === selected_grade) {
                    rows[i].style.display = 'table-row';

                }else {
                    rows[i].style.display = 'none';
                }
            }


        }
    }
}


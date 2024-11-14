/**
 * 
 * JS DASHBORD GRAPHIC-INFOS BUSNESS
 */
// <!-- Charts; Dark Mode -->
    function toggleDarkMode() {
      document.body.classList.toggle('dark-mode');
      updateChartsTheme();
    }

    function updateChartsTheme() {
      const isDarkMode = document.body.classList.contains('dark-mode');
      const textColor = isDarkMode ? '#ffffff' : '#333333';
      
      Chart.helpers.each(Chart.instances, function(instance){
        instance.options.scales.x.ticks.color = textColor;
        instance.options.scales.y.ticks.color = textColor;
        instance.options.plugins.legend.labels.color = textColor;
        instance.update();
      });
    }

    // // Genre Popularity Chart
    // const genrePopularityCtx = document.getElementById('genrePopularityChart').getContext('2d');

    // new Chart(genrePopularityCtx, {
    //   type: 'bar',
    //   data: {
    //     labels: ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror'],
    //     datasets: [{
    //       label: 'Genre Popularity',
    //       data: [65, 59, 80, 81, 56],
    //       backgroundColor: [
    //         'rgba(255, 99, 132, 0.6)',
    //         'rgba(54, 162, 235, 0.6)',
    //         'rgba(255, 206, 86, 0.6)',
    //         'rgba(75, 192, 192, 0.6)',
    //         'rgba(153, 102, 255, 0.6)'
    //       ],
    //     }]
    //   },
    //   options: {
    //     responsive: true,
    //     plugins: {
    //       legend: {
    //         position: 'top',
    //       },
    //       title: {
    //         display: true,
    //         text: 'Genre Popularity'
    //       }
    //     }
    //   }
    // });

    // Infos Commandes Chart pie cercle: compare les commandes traitees et non traitees
    const InfosCommandesPie = document.getElementById('InfosCommandesPieChart').getContext('2d');
    new Chart(InfosCommandesPie, {
      type: 'doughnut',
      data: {
        labels: ['Traiter', 'Non Traiter'],
        datasets: [{
          data: [30, 50],
          backgroundColor: [
            '#0A21C0',
            '#050A44',
          ],
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Infos Commandes'
          }
        }
      }
    });

    // Prédiction des ventes : prédiction des revenus et des commandes
    const PredictionVentes = document.getElementById('PredictionVentesChart').getContext('2d');
    new Chart(PredictionVentes, {
      type: 'line',
      data: {
        labels: ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Jui', 'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec'],
        datasets: [{
          label: 'Revenu',
          data: [12, 19, 3, 5, 2, 3, 10, 7, 4, 6, 8, 9],
          borderColor: '#141619',
          tension: 0.1
        },
        {
          label: 'Commandes',
          data: [2, 3, 20, 5, 1, 4, 10, 7, 12, 20, 8, 30],
          borderColor: '#B3B4BD',
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Prédiction des ventes'
          }
        }
      }
    });

    // // AI Usage Chart
    // const aiUsageCtx = document.getElementById('aiUsageChart').getContext('2d');
    // new Chart(aiUsageCtx, {
    //   type: 'radar',
    //   data: {
    //     labels: ['Script Generation', 'Character Design', 'Plot Analysis', 'Dialogue Enhancement', 'Scene Description'],
    //     datasets: [{
    //       label: 'AI Usage',
    //       data: [65, 59, 90, 81, 56],
    //       fill: true,
    //       backgroundColor: 'rgba(255, 99, 132, 0.2)',
    //       borderColor: 'rgb(255, 99, 132)',
    //       pointBackgroundColor: 'rgb(255, 99, 132)',
    //       pointBorderColor: '#fff',
    //       pointHoverBackgroundColor: '#fff',
    //       pointHoverBorderColor: 'rgb(255, 99, 132)'
    //     }]
    //   },
    //   options: {
    //     responsive: true,
    //     plugins: {
    //       legend: {
    //         position: 'top',
    //       },
    //       title: {
    //         display: true,
    //         text: 'AI Usage in Production'
    //       }
    //     }
    //   }
    // });

    // Revenue Chart: Revenue generé par mois
    const revenueCtx = document.getElementById('revenueChart').getContext('2d');
    new Chart(revenueCtx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin'],
        datasets: [{
          label: 'Revenue',
          data: [1000000, 1200000, 900000, 1500000, 2000000, 2400000],
          borderColor: '#0A21C0',
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: ' Revenue generé par mois'
          }
        }
      }
    });

    // // Team Performance Chart
    // const teamPerformanceCtx = document.getElementById('teamPerformanceChart').getContext('2d');
    // new Chart(teamPerformanceCtx, {
    //   type: 'bar',
    //   data: {
    //     labels: ['Writing', 'Design', 'Animation', 'Sound', 'Marketing'],
    //     datasets: [{
    //       label: 'Team Performance',
    //       data: [85, 72, 90, 78, 88],
    //       backgroundColor: [
    //         'rgba(255, 99, 132, 0.6)',
    //         'rgba(54, 162, 235, 0.6)',
    //         'rgba(255, 206, 86, 0.6)',
    //         'rgba(75, 192, 192, 0.6)',
    //         'rgba(153, 102, 255, 0.6)'
    //       ],
    //     }]
    //   },
    //   options: {
    //     responsive: true,
    //     plugins: {
    //       legend: {
    //         position: 'top',
    //       },
    //       title: {
    //         display: true,
    //         text: 'Team Performance'
    //       }
    //     }
    //   }
    // });

    updateChartsTheme();

// -----------------------------------------------------

//   <!-- Calendars -->
    class DatePicker {
      constructor() {
        this.currentDate = new Date();
        this.selectedDate = null;
        this.rangeStart = null;
        this.rangeEnd = null;
        this.isRange = false;
        this.isOpen = false;
        
        // DOM elements
        this.calendar = document.getElementById('calendar');
        this.monthYear = document.getElementById('monthYear');
        this.daysGrid = document.getElementById('daysGrid');
        this.selectedDateDisplay = document.getElementById('selectedDateDisplay');
        this.datePickerBtn = document.getElementById('datePickerBtn');
        
        // Event listeners
        document.getElementById('prevMonth').addEventListener('click', (e) => {
          e.stopPropagation();
          this.navigateMonth(-1);
        });
        document.getElementById('nextMonth').addEventListener('click', (e) => {
          e.stopPropagation();
          this.navigateMonth(1);
        });
        document.getElementById('singleMode').addEventListener('change', () => this.setMode(false));
        document.getElementById('rangeMode').addEventListener('change', () => this.setMode(true));
        document.getElementById('cancelBtn').addEventListener('click', (e) => {
          e.stopPropagation();
          this.hideCalendar();
        });
        document.getElementById('applyBtn').addEventListener('click', (e) => {
          e.stopPropagation();
          this.applySelection();
        });
        this.datePickerBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.toggleCalendar();
        });
        
        // Close calendar when clicking outside
        document.addEventListener('click', (e) => {
          if (this.isOpen && !this.calendar.contains(e.target) && e.target !== this.datePickerBtn) {
            this.hideCalendar();
          }
        });
        
        // Prevent calendar from closing when clicking inside
        this.calendar.addEventListener('click', (e) => {
          e.stopPropagation();
        });
        
        this.render();
      }
      
      setMode(isRange) {
        this.isRange = isRange;
        this.selectedDate = null;
        this.rangeStart = null;
        this.rangeEnd = null;
        this.render();
      }
      
      toggleCalendar() {
        if (!this.isOpen) {
          const rect = this.datePickerBtn.getBoundingClientRect();
          this.calendar.style.top = `${rect.bottom + window.scrollY + 5}px`;
          this.calendar.style.left = `${rect.left + window.scrollX}px`;
          this.calendar.style.display = 'block';
          this.isOpen = true;
        } else {
          this.hideCalendar();
        }
      }
      
      hideCalendar() {
        this.calendar.style.display = 'none';
        this.isOpen = false;
      }
      
      applySelection() {
        if (this.isRange) {
          if (this.rangeStart && this.rangeEnd) {
            this.selectedDateDisplay.value = `${this.formatDate(this.rangeStart)} - ${this.formatDate(this.rangeEnd)}`;
            this.hideCalendar();
          }
        } else if (this.selectedDate) {
          this.selectedDateDisplay.value = this.formatDate(this.selectedDate);
          this.hideCalendar();
        }
      }
      
      formatDate(date) {
        return date.toLocaleDateString();
      }
      
      navigateMonth(delta) {
        this.currentDate.setMonth(this.currentDate.getMonth() + delta);
        this.render();
      }
      
      handleDateClick(date) {
        if (this.isRange) {
          if (!this.rangeStart || (this.rangeStart && this.rangeEnd)) {
            this.rangeStart = date;
            this.rangeEnd = null;
          } else {
            if (date < this.rangeStart) {
              this.rangeEnd = this.rangeStart;
              this.rangeStart = date;
            } else {
              this.rangeEnd = date;
            }
          }
        } else {
          this.selectedDate = date;
        }
        this.render();
      }
      
      isInRange(date) {
        if (!this.isRange || !this.rangeStart || !this.rangeEnd) return false;
        return date >= this.rangeStart && date <= this.rangeEnd;
      }
      
      render() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        // Update header
        const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December'];
        this.monthYear.textContent = `${monthNames[month]} ${year}`;
        
        // Clear grid
        this.daysGrid.innerHTML = '';
        
        // Get first day of month and total days
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        
        // Add empty cells for days before first of month
        for (let i = 0; i < firstDay; i++) {
          const emptyDay = document.createElement('div');
          emptyDay.className = 'day disabled';
          this.daysGrid.appendChild(emptyDay);
        }
        
        // Add days of month
        const today = new Date();
        for (let day = 1; day <= daysInMonth; day++) {
          const currentDate = new Date(year, month, day);
          const dayEl = document.createElement('div');
          dayEl.className = 'day';
          dayEl.textContent = day;
          
          if (this.isRange) {
            if (this.isInRange(currentDate)) {
              dayEl.classList.add('in-range');
            }
            if (this.rangeStart && currentDate.getTime() === this.rangeStart.getTime()) {
              dayEl.classList.add('range-start');
            }
            if (this.rangeEnd && currentDate.getTime() === this.rangeEnd.getTime()) {
              dayEl.classList.add('range-end');
            }
          } else if (this.selectedDate && 
                    currentDate.getTime() === this.selectedDate.getTime()) {
            dayEl.classList.add('selected');
          }
          
          if (year === today.getFullYear() && 
              month === today.getMonth() && 
              day === today.getDate()) {
            dayEl.classList.add('today');
          }
          
          dayEl.addEventListener('click', (e) => {
            e.stopPropagation();
            this.handleDateClick(currentDate);
          });
          this.daysGrid.appendChild(dayEl);
        }
      }
    }
    
    // Initialize date picker
    const datePicker = new DatePicker();
    toggleDarkMode();
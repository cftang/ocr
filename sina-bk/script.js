const minutesDisplay = document.getElementById('minutes');
const secondsDisplay = document.getElementById('seconds');
const startBtn = document.getElementById('start-btn');
const resetBtn = document.getElementById('reset-btn');
const workModeBtn = document.getElementById('work-mode');
const breakModeBtn = document.getElementById('break-mode');
const longBreakModeBtn = document.getElementById('long-break-mode');
const container = document.querySelector('.timer-display');
const workTimeInput = document.getElementById('work-time');
const breakTimeInput = document.getElementById('break-time');
const longBreakTimeInput = document.getElementById('long-break-time');
const cyclesInput = document.getElementById('cycles-count');
const currentRoundDisplay = document.getElementById('current-round');
const totalRoundsDisplay = document.getElementById('total-rounds');
const historyList = document.getElementById('history-list');

let timerInterval;
let timeLeft;
let isRunning = false;
let currentMode = 'work'; // 'work', 'short-break', 'long-break'
let currentRound = 1;
let sessionStartTime = null;

// Request notification permission immediately
if (Notification.permission !== 'granted' && Notification.permission !== 'denied') {
    Notification.requestPermission();
}

function getSettings() {
    return {
        work: parseInt(workTimeInput.value) * 60,
        shortBreak: parseInt(breakTimeInput.value) * 60,
        longBreak: parseInt(longBreakTimeInput.value) * 60,
        rounds: parseInt(cyclesInput.value)
    };
}

// Initialize
timeLeft = getSettings().work;
updateRoundDisplay();

function updateRoundDisplay() {
    const settings = getSettings();
    currentRoundDisplay.textContent = currentRound;
    totalRoundsDisplay.textContent = settings.rounds;
}

function updateDisplay() {
    const m = Math.floor(timeLeft / 60);
    const s = timeLeft % 60;
    minutesDisplay.textContent = m.toString().padStart(2, '0');
    secondsDisplay.textContent = s.toString().padStart(2, '0');

    // Update title
    let modeText = currentMode === 'work' ? 'Work' : (currentMode === 'long-break' ? 'Long Break' : 'Short Break');
    document.title = `${minutesDisplay.textContent}:${secondsDisplay.textContent} - ${modeText}`;
}

function formatTime(date) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

function logHistory(mode, start, end) {
    const li = document.createElement('li');
    let modeLabel = mode === 'work' ? 'Work' : (mode === 'long-break' ? 'Long Break' : 'Short Break');
    let colorClass = mode === 'work' ? '#6366f1' : (mode === 'long-break' ? '#ec4899' : '#06b6d4');

    li.innerHTML = `
        <span class="mode-label" style="color: ${colorClass}">${modeLabel}</span>
        <span class="time-span">${formatTime(start)} - ${formatTime(end)}</span>
    `;

    // Prepend to show newest first
    if (historyList.firstChild) {
        historyList.insertBefore(li, historyList.firstChild);
    } else {
        historyList.appendChild(li);
    }
}

function switchMode(mode) {
    clearInterval(timerInterval);
    isRunning = false;
    currentMode = mode;
    sessionStartTime = null; // Reset start time on manual switch

    const settings = getSettings();

    // Reset active classes
    workModeBtn.classList.remove('active');
    breakModeBtn.classList.remove('active');
    longBreakModeBtn.classList.remove('active');

    if (mode === 'work') {
        timeLeft = settings.work;
        workModeBtn.classList.add('active');
        document.documentElement.style.setProperty('--accent-color', '#6366f1');
    } else if (mode === 'short-break') {
        timeLeft = settings.shortBreak;
        breakModeBtn.classList.add('active');
        document.documentElement.style.setProperty('--accent-color', '#06b6d4');
    } else if (mode === 'long-break') {
        timeLeft = settings.longBreak;
        longBreakModeBtn.classList.add('active');
        document.documentElement.style.setProperty('--accent-color', '#ec4899'); // Pink for long break
    }

    startBtn.textContent = 'Start';
    container.classList.add('paused');
    updateDisplay();
    updateRoundDisplay();
}

function notifyUser(nextMode) {
    const settings = getSettings();
    let title, body;

    if (nextMode === 'work') {
        title = currentMode === 'long-break' ? 'Long Break Over!' : 'Short Break Over!';
        body = `Next: Work (${settings.work / 60}m)`;
    } else if (nextMode === 'long-break') {
        title = 'Work Session Complete!';
        body = `Next: Long Break (${settings.longBreak / 60}m)`;
    } else {
        title = 'Work Session Complete!';
        body = `Next: Short Break (${settings.shortBreak / 60}m)`;
    }

    if (Notification.permission === "granted") {
        const notification = new Notification(title, {
            body: body,
            icon: 'https://cdn-icons-png.flaticon.com/512/3209/3209955.png', // Generic timer icon
            requireInteraction: false // Auto-close notification (default behavior)
        });

        notification.onclick = function () {
            window.focus(); // Bring window to front
            this.close();   // Close notification
        };
    }
}

function startTimer() {
    if (isRunning) {
        // Pause logic
        clearInterval(timerInterval);
        isRunning = false;
        startBtn.textContent = 'Start';
        container.classList.add('paused');
        // Note: We don't clear sessionStartTime here, so resuming keeps the original start time
        // Or should we? If I pause for an hour, the "Start - End" log will look weird (10:00 - 11:25 for a 25m session).
        // Standard behavior: Keep original start time? Or log "segment"?
        // Let's reset start time on resume for accuracy of *this specific interval run*?
        // No, let's keep it simple. sessionStartTime is set when we START from a non-running state.
    } else {
        // Start logic
        // Check permission again if not granted
        if (Notification.permission === 'default') {
            Notification.requestPermission();
        }

        isRunning = true;
        startBtn.textContent = 'Pause';
        container.classList.remove('paused');

        // If this is a fresh start (not a resume from pause), set start time
        // Actually, simple logic: if sessionStartTime is null, set it.
        // Wait, if I manual reset, sessionStartTime becomes null.
        if (!sessionStartTime) {
            sessionStartTime = new Date();
        }

        timerInterval = setInterval(() => {
            if (timeLeft > 0) {
                timeLeft--;
                updateDisplay();
            } else {
                clearInterval(timerInterval);
                const settings = getSettings();

                // Log history on completion
                logHistory(currentMode, sessionStartTime, new Date());
                sessionStartTime = null; // Clear for next session

                let nextMode;

                // Cycle Logic
                if (currentMode === 'work') {
                    if (currentRound < settings.rounds) {
                        nextMode = 'short-break';
                    } else {
                        nextMode = 'long-break';
                    }
                } else if (currentMode === 'short-break') {
                    currentRound++;
                    nextMode = 'work';
                } else if (currentMode === 'long-break') {
                    currentRound = 1;
                    nextMode = 'work';
                }

                notifyUser(nextMode);
                switchMode(nextMode); // switchMode resets isRunning to false and clears interval

                // Auto-start next mode
                // switchMode sets sessionStartTime to null, so startTimer will set a NEW start time
                startTimer();
            }
        }, 1000);
    }
}

function resetTimer() {
    clearInterval(timerInterval);
    isRunning = false;
    sessionStartTime = null; // Clear history tracking
    startBtn.textContent = 'Start';
    container.classList.add('paused');

    // Reset to initial state
    currentRound = 1;
    currentMode = 'work';

    const settings = getSettings();
    timeLeft = settings.work;

    workModeBtn.classList.add('active');
    breakModeBtn.classList.remove('active');
    longBreakModeBtn.classList.remove('active');
    document.documentElement.style.setProperty('--accent-color', '#6366f1');

    updateDisplay();
    updateRoundDisplay();
}

// Event Listeners
startBtn.addEventListener('click', startTimer);
resetBtn.addEventListener('click', resetTimer);

workModeBtn.addEventListener('click', () => {
    switchMode('work');
});
breakModeBtn.addEventListener('click', () => {
    switchMode('short-break');
});
longBreakModeBtn.addEventListener('click', () => {
    switchMode('long-break');
});

// Update logic when inputs change
function handleInputChange() {
    if (isRunning) return;

    const settings = getSettings();
    totalRoundsDisplay.textContent = settings.rounds;

    if (currentMode === 'work') timeLeft = settings.work;
    if (currentMode === 'short-break') timeLeft = settings.shortBreak;
    if (currentMode === 'long-break') timeLeft = settings.longBreak;

    updateDisplay();
}

[workTimeInput, breakTimeInput, longBreakTimeInput, cyclesInput].forEach(input => {
    input.addEventListener('change', handleInputChange);
});

// Initial display
updateDisplay();
container.classList.add('paused');

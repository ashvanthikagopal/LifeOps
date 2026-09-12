import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8000";


function App() {

  const [tasks, setTasks] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");


  // =====================================================
  // FETCH TASKS
  // =====================================================

  async function fetchTasks() {

    try {

      setError("");

      const response = await fetch(
        `${API_URL}/tasks/`
      );

      if (!response.ok) {
        throw new Error(
          "Unable to load tasks."
        );
      }

      const data = await response.json();

      setTasks(data);

    } catch (error) {

      setError(error.message);

    } finally {

      setLoading(false);

    }
  }


  // =====================================================
  // INITIAL LOAD
  // =====================================================

  useEffect(() => {

    fetchTasks();

  }, []);


  // =====================================================
  // AUTO REFRESH
  // =====================================================

  useEffect(() => {

    const interval = setInterval(
      fetchTasks,
      5000
    );

    return () => clearInterval(interval);

  }, []);


  // =====================================================
  // APPROVE
  // =====================================================

  async function approveTask(taskId) {

    try {

      const response = await fetch(
        `${API_URL}/tasks/${taskId}/approve`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Unable to approve task."
        );
      }

      await fetchTasks();

    } catch (error) {

      alert(error.message);

    }
  }


  // =====================================================
  // REJECT
  // =====================================================

  async function rejectTask(taskId) {

    try {

      const response = await fetch(
        `${API_URL}/tasks/${taskId}/reject`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Unable to reject task."
        );
      }

      await fetchTasks();

    } catch (error) {

      alert(error.message);

    }
  }


  // =====================================================
  // EXECUTE
  // =====================================================

  async function executeTask(taskId) {

    try {

      const response = await fetch(
        `${API_URL}/tasks/${taskId}/execute`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Unable to execute action."
        );
      }

      await fetchTasks();

    } catch (error) {

      alert(error.message);

    }
  }


  // =====================================================
  // VERIFY
  // =====================================================

  async function verifyTask(taskId) {

    const confirmed = window.confirm(
      "Have you actually completed this task?"
    );

    if (!confirmed) {
      return;
    }

    try {

      const response = await fetch(
        `${API_URL}/tasks/${taskId}/verify`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({

            evidence:
              "User explicitly confirmed task completion.",

            source:
              "USER_CONFIRMATION",

          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Unable to verify task."
        );
      }

      await fetchTasks();

    } catch (error) {

      alert(error.message);

    }
  }


  // =====================================================
  // FILTERS
  // =====================================================

  const approvalTasks = tasks.filter(
    (task) =>
      task.status === "PENDING" &&
      task.approval_status === "PENDING"
  );


  const reminderTasks = tasks.filter(
    (task) =>
      task.status === "PENDING" &&
      task.approval_status !== "PENDING"
  );


  const completedTasks = tasks.filter(
    (task) =>
      task.status === "COMPLETED"
  );


  const rejectedTasks = tasks.filter(
    (task) =>
      task.status === "REJECTED"
  );


  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {

    return (
      <div className="loading">
        Loading LifeOps...
      </div>
    );

  }


  // =====================================================
  // UI
  // =====================================================

  return (

    <div className="app">

      {/* HEADER */}

      <header className="header">

        <div>

          <h1>LifeOps</h1>

          <p>
            Don't ask me unless you have to.
          </p>

        </div>


        <button
          className="refresh-button"
          onClick={fetchTasks}
        >
          Refresh
        </button>

      </header>


      {/* ERROR */}

      {error && (

        <div className="error">
          {error}
        </div>

      )}


      {/* STATS */}

      <section className="stats">

        <StatCard
          label="Needs Approval"
          value={approvalTasks.length}
        />

        <StatCard
          label="Reminders"
          value={reminderTasks.length}
        />

        <StatCard
          label="Completed"
          value={completedTasks.length}
        />

      </section>


      {/* APPROVAL */}

      <TaskSection
        title="Needs Your Approval"
        count={approvalTasks.length}
        emptyMessage="Nothing requires your approval."
      >

        {approvalTasks.map(
          (task) => (

            <TaskCard
              key={task.id}
              task={task}
              onApprove={approveTask}
              onReject={rejectTask}
              onExecute={executeTask}
              onVerify={verifyTask}
            />

          )
        )}

      </TaskSection>


      {/* REMINDERS */}

      <TaskSection
        title="Reminders"
        count={reminderTasks.length}
        emptyMessage="No pending reminders."
      >

        {reminderTasks.map(
          (task) => (

            <TaskCard
              key={task.id}
              task={task}
              onApprove={approveTask}
              onReject={rejectTask}
              onExecute={executeTask}
              onVerify={verifyTask}
            />

          )
        )}

      </TaskSection>


      {/* COMPLETED */}

      <TaskSection
        title="Completed"
        count={completedTasks.length}
        emptyMessage="No completed tasks yet."
      >

        {completedTasks.map(
          (task) => (

            <TaskCard
              key={task.id}
              task={task}
              onApprove={approveTask}
              onReject={rejectTask}
              onExecute={executeTask}
              onVerify={verifyTask}
            />

          )
        )}

      </TaskSection>


      {/* REJECTED */}

      {rejectedTasks.length > 0 && (

        <TaskSection
          title="Rejected"
          count={rejectedTasks.length}
          emptyMessage=""
        >

          {rejectedTasks.map(
            (task) => (

              <TaskCard
                key={task.id}
                task={task}
                onApprove={approveTask}
                onReject={rejectTask}
                onExecute={executeTask}
                onVerify={verifyTask}
              />

            )
          )}

        </TaskSection>

      )}

    </div>
  );
}


// =====================================================
// STAT CARD
// =====================================================

function StatCard({
  label,
  value
}) {

  return (

    <div className="stat-card">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>

  );
}


// =====================================================
// SECTION
// =====================================================

function TaskSection({
  title,
  count,
  emptyMessage,
  children
}) {

  return (

    <section className="section">

      <div className="section-header">

        <h2>
          {title}
        </h2>

        <span>
          {count}
        </span>

      </div>


      {count === 0 ? (

        <div className="empty-state">
          {emptyMessage}
        </div>

      ) : (

        children

      )}

    </section>

  );
}


// =====================================================
// TASK CARD
// =====================================================

function TaskCard({
  task,
  onApprove,
  onReject,
  onExecute,
  onVerify
}) {

  const isApprovalRequired =
    task.status === "PENDING" &&
    task.approval_status === "PENDING";


  const isReminder =
    task.status === "PENDING" &&
    task.approval_status !== "PENDING";


  const isApproved =
    task.approval_status === "APPROVED";


  const actionCompleted =
    task.action_status === "COMPLETED";


  const isCompleted =
    task.status === "COMPLETED";


  return (

    <div className="task-card">

      <div className="task-main">

        <div className="task-title-row">

          <h3>
            {task.title}
          </h3>

          <span
            className={
              `risk risk-${task.risk_level.toLowerCase()}`
            }
          >
            {task.risk_level}
          </span>

        </div>


        <p>
          {task.description}
        </p>


        <div className="task-meta">

          <span>
            Action: {task.action_type}
          </span>

          <span>
            Approval: {task.approval_status}
          </span>

          <span>
            LifeOps Action: {task.action_status}
          </span>

          <span>
            Task: {task.status}
          </span>

        </div>


        {/* REMINDER MESSAGE */}

        {isReminder &&
          !isCompleted && (

            <div className="reminder-message">

              🔔 Your task is still pending.

              {actionCompleted && (
                <span>
                  {" "}
                  LifeOps has already handled
                  its action.
                </span>
              )}

            </div>

          )}


        {/* COMPLETION */}

        {task.completion_source && (

          <div className="verification">

            ✓ Completion verified by{" "}
            {task.completion_source}

          </div>

        )}

      </div>


      {/* ACTION BUTTONS */}

      <div className="task-actions">


        {/* APPROVAL */}

        {isApprovalRequired && (

          <>

            <button
              className="approve-button"
              onClick={() =>
                onApprove(task.id)
              }
            >
              Approve
            </button>


            <button
              className="reject-button"
              onClick={() =>
                onReject(task.id)
              }
            >
              Reject
            </button>

          </>

        )}


        {/* EXECUTE AFTER APPROVAL */}

        {isApproved &&
          !actionCompleted &&
          !isCompleted && (

            <button
              className="execute-button"
              onClick={() =>
                onExecute(task.id)
              }
            >
              Execute
            </button>

          )}


        {/* VERIFY */}

        {isReminder &&
          !isCompleted && (

            <button
              className="verify-button"
              onClick={() =>
                onVerify(task.id)
              }
            >
              I've Completed This
            </button>

          )}

      </div>

    </div>

  );
}


export default App;
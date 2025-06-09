import { useState, useEffect } from 'react';
import type { Task, Priority } from './types';
import {
  Container,
  Typography,
  TextField,
  Button,
  List,
  ListItem,
  Checkbox,
  IconButton,
  Box,
  Paper,
  ListItemText,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
} from '@mui/material';
import type { SelectChangeEvent } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

const getPriorityColor = (priority: Priority) => {
  switch (priority) {
    case 'High':
      return 'error';
    case 'Medium':
      return 'warning';
    case 'Low':
      return 'success';
    default:
      return 'default';
  }
};

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskPriority, setNewTaskPriority] = useState<Priority>('Medium');

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch('/data.json');
        if (response.ok) {
          const data = await response.json();
          setTasks(data);
        } else {
          setTasks([]);
        }
      } catch (error) {
        console.error('Failed to load tasks:', error);
        setTasks([]);
      }
    };
    fetchTasks();
  }, []);

  const handleAddTask = () => {
    if (newTaskTitle.trim() === '') return;
    const newTask: Task = {
      id: Date.now(),
      title: newTaskTitle,
      completed: false,
      priority: newTaskPriority,
    };
    setTasks(prevTasks => [newTask, ...prevTasks]);
    setNewTaskTitle('');
    setNewTaskPriority('Medium');
  };

  const handleToggleComplete = (id: number) => {
    setTasks(prevTasks =>
      prevTasks.map(task =>
        task.id === id ? { ...task, completed: !task.completed } : task
      )
    );
  };

  const handleDeleteTask = (id: number) => {
    setTasks(prevTasks => prevTasks.filter(task => task.id !== id));
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" gutterBottom color="primary" data-testid="main-heading">
          To-Do List
        </Typography>
        
        <Paper elevation={2} sx={{ p: 3, width: '100%', mb: 3 }} data-testid="add-task-form">
          <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="What needs to be done?"
              value={newTaskTitle}
              onChange={e => setNewTaskTitle(e.target.value)}
              onKeyPress={e => e.key === 'Enter' && handleAddTask()}
              sx={{ mr: 2 }}
              data-testid="add-task-input"
            />
            <FormControl sx={{ minWidth: 120, mr: 2 }}>
              <InputLabel id="priority-select-label">Priority</InputLabel>
              <Select
                labelId="priority-select-label"
                id="priority-select"
                value={newTaskPriority}
                label="Priority"
                onChange={(e: SelectChangeEvent<Priority>) => setNewTaskPriority(e.target.value as Priority)}
                data-testid="priority-select"
              >
                <MenuItem value="Low">Low</MenuItem>
                <MenuItem value="Medium">Medium</MenuItem>
                <MenuItem value="High">High</MenuItem>
              </Select>
            </FormControl>
            <Button
              variant="contained"
              onClick={handleAddTask}
              sx={{ whiteSpace: 'nowrap' }}
              data-testid="add-task-button"
            >
              Add Task
            </Button>
          </Box>
        </Paper>

        <Box sx={{ width: '100%' }}>
          {tasks.length === 0 ? (
            <Paper elevation={1} sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="body1" color="text.secondary">
                No tasks yet. Add one above to get started!
              </Typography>
            </Paper>
          ) : (
            <List sx={{ width: '100%', p: 0 }} data-testid="task-list">
              {tasks.map(task => (
                <ListItem
                  key={task.id}
                  data-testid={`task-item-${task.id}`}
                  disablePadding
                  sx={{ 
                    mb: 1,
                    '&:hover': { backgroundColor: 'action.hover' }
                  }}
                  secondaryAction={
                    <IconButton 
                      edge="end" 
                      aria-label="delete" 
                      onClick={() => handleDeleteTask(task.id)}
                      color="error"
                      data-testid={`task-item-delete-button-${task.id}`}
                    >
                      <DeleteIcon />
                    </IconButton>
                  }
                >
                  <Checkbox
                    edge="start"
                    checked={task.completed}
                    tabIndex={-1}
                    disableRipple
                    onChange={() => handleToggleComplete(task.id)}
                    color="primary"
                    data-testid={`task-item-checkbox-${task.id}`}
                  />
                  <ListItemText
                    primary={task.title}
                    data-testid={`task-item-label-${task.id}`}
                    sx={{
                      '& .MuiListItemText-primary': {
                        textDecoration: task.completed ? 'line-through' : 'none',
                        color: task.completed ? 'text.secondary' : 'text.primary',
                      }
                    }}
                  />
                  <Chip 
                    label={task.priority} 
                    color={getPriorityColor(task.priority)}
                    size="small"
                    sx={{
                      minWidth: '70px',
                      fontWeight: 'bold',
                      mr: 8
                    }}
                  />
                </ListItem>
              ))}
            </List>
          )}
        </Box>
      </Box>
    </Container>
  );
}

export default App;

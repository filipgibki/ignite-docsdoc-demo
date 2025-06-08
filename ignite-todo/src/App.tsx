import { useState, useEffect } from 'react';
import type { Task } from './types';
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
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');

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
    };
    setTasks(prevTasks => [newTask, ...prevTasks]);
    setNewTaskTitle('');
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
        <Typography variant="h4" component="h1" gutterBottom color="primary">
          To-Do List
        </Typography>
        
        <Paper elevation={2} sx={{ p: 3, width: '100%', mb: 3 }}>
          <Box sx={{ display: 'flex', width: '100%' }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="What needs to be done?"
              value={newTaskTitle}
              onChange={e => setNewTaskTitle(e.target.value)}
              onKeyPress={e => e.key === 'Enter' && handleAddTask()}
            />
            <Button
              variant="contained"
              onClick={handleAddTask}
              sx={{ ml: 2, whiteSpace: 'nowrap' }}
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
            <List sx={{ width: '100%', p: 0 }}>
              {tasks.map(task => (
                <ListItem
                  key={task.id}
                  disablePadding
                  sx={{ mb: 1 }}
                  secondaryAction={
                    <IconButton 
                      edge="end" 
                      aria-label="delete" 
                      onClick={() => handleDeleteTask(task.id)}
                      color="error"
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
                  />
                  <ListItemText
                    primary={task.title}
                    sx={{
                      '& .MuiListItemText-primary': {
                        textDecoration: task.completed ? 'line-through' : 'none',
                        color: task.completed ? 'text.secondary' : 'text.primary',
                      }
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

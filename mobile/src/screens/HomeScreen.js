import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  RefreshControl,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Avatar,
  Surface,
  Chip,
  ProgressBar,
} from 'react-native-paper';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import { historyAPI, companyAPI } from '../services/api';

const screenWidth = Dimensions.get('window').width;

export default function HomeScreen({ navigation }) {
  const { user, token } = useAuth();
  const [refreshing, setRefreshing] = useState(false);
  const [stats, setStats] = useState({
    totalAnalyses: 0,
    averageScore: 0,
    topCompanies: [],
    recentTrends: [],
    skillGaps: [],
  });
  const [jobStats, setJobStats] = useState({
    totalCompanies: 0,
    totalJobs: 0,
    lastUpdated: null,
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      // Load user analytics
      const trends = await historyAPI.getAnalysisTrends(token);
      if (!trends.error) {
        setStats({
          totalAnalyses: trends.score_trends?.length || 0,
          averageScore: trends.score_trends?.[0]?.avg_score || 0,
          topCompanies: trends.top_companies || [],
          recentTrends: trends.score_trends || [],
          skillGaps: trends.most_needed_skills || [],
        });
      }

      // Load job market stats
      const jobData = await companyAPI.getJobDataStats();
      if (!jobData.error) {
        setJobStats(jobData);
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadDashboardData();
    setRefreshing(false);
  };

  const chartData = {
    labels: stats.recentTrends.slice(0, 7).reverse().map(t => 
      new Date(t.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    ),
    datasets: [
      {
        data: stats.recentTrends.slice(0, 7).reverse().map(t => t.avg_score),
        color: (opacity = 1) => `rgba(134, 65, 244, ${opacity})`,
        strokeWidth: 2,
      },
    ],
  };

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Welcome Section */}
      <Card style={styles.welcomeCard}>
        <Card.Content style={styles.welcomeContent}>
          <Avatar.Text
            size={60}
            label={user?.first_name?.[0] || user?.email?.[0] || 'U'}
            style={styles.avatar}
          />
          <View style={styles.welcomeText}>
            <Title style={styles.welcomeTitle}>
              Welcome back, {user?.first_name || 'User'}!
            </Title>
            <Paragraph style={styles.welcomeSubtitle}>
              Ready to analyze your resume and boost your career?
            </Paragraph>
          </View>
        </Card.Content>
      </Card>

      {/* Quick Stats */}
      <View style={styles.statsRow}>
        <Surface style={styles.statCard}>
          <Title style={styles.statNumber}>{stats.totalAnalyses}</Title>
          <Paragraph style={styles.statLabel}>Analyses</Paragraph>
        </Surface>
        <Surface style={styles.statCard}>
          <Title style={styles.statNumber}>{stats.averageScore}%</Title>
          <Paragraph style={styles.statLabel}>Avg Score</Paragraph>
        </Surface>
        <Surface style={styles.statCard}>
          <Title style={styles.statNumber}>{jobStats.totalCompanies}</Title>
          <Paragraph style={styles.statLabel}>Companies</Paragraph>
        </Surface>
      </View>

      {/* Progress Chart */}
      {stats.recentTrends.length > 0 && (
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>Your Progress</Title>
            <LineChart
              data={chartData}
              width={screenWidth - 60}
              height={200}
              chartConfig={{
                backgroundColor: '#ffffff',
                backgroundGradientFrom: '#ffffff',
                backgroundGradientTo: '#ffffff',
                decimalPlaces: 0,
                color: (opacity = 1) => `rgba(134, 65, 244, ${opacity})`,
                labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                style: {
                  borderRadius: 16,
                },
                propsForDots: {
                  r: '4',
                  strokeWidth: '2',
                  stroke: '#8641f4',
                },
              }}
              bezier
              style={styles.chart}
            />
          </Card.Content>
        </Card>
      )}

      {/* Top Companies */}
      {stats.topCompanies.length > 0 && (
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>Your Top Companies</Title>
            {stats.topCompanies.slice(0, 3).map((company, index) => (
              <View key={index} style={styles.companyItem}>
                <View style={styles.companyInfo}>
                  <Paragraph style={styles.companyName}>{company.company}</Paragraph>
                  <Paragraph style={styles.companyStats}>
                    {company.analysis_count} analyses • {company.avg_score}% avg
                  </Paragraph>
                </View>
                <ProgressBar
                  progress={company.avg_score / 100}
                  color="#8641f4"
                  style={styles.progressBar}
                />
              </View>
            ))}
          </Card.Content>
        </Card>
      )}

      {/* Skill Gaps */}
      {stats.skillGaps.length > 0 && (
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>Skills to Focus On</Title>
            <View style={styles.skillsContainer}>
              {stats.skillGaps.slice(0, 6).map((skill, index) => (
                <Chip
                  key={index}
                  style={styles.skillChip}
                  textStyle={styles.skillChipText}
                >
                  {skill.skill}
                </Chip>
              ))}
            </View>
          </Card.Content>
        </Card>
      )}

      {/* Quick Actions */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.cardTitle}>Quick Actions</Title>
          <View style={styles.actionButtons}>
            <Button
              mode="contained"
              onPress={() => navigation.navigate('Upload')}
              style={styles.actionButton}
              icon="cloud-upload"
            >
              Upload Resume
            </Button>
            <Button
              mode="outlined"
              onPress={() => navigation.navigate('Analysis')}
              style={styles.actionButton}
              icon="analytics"
            >
              Analyze Companies
            </Button>
            <Button
              mode="outlined"
              onPress={() => navigation.navigate('Interview')}
              style={styles.actionButton}
              icon="microphone"
            >
              Practice Interview
            </Button>
          </View>
        </Card.Content>
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  welcomeCard: {
    margin: 16,
    marginBottom: 8,
  },
  welcomeContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  avatar: {
    marginRight: 16,
  },
  welcomeText: {
    flex: 1,
  },
  welcomeTitle: {
    fontSize: 20,
    marginBottom: 4,
  },
  welcomeSubtitle: {
    fontSize: 14,
    opacity: 0.7,
  },
  statsRow: {
    flexDirection: 'row',
    marginHorizontal: 16,
    marginBottom: 8,
  },
  statCard: {
    flex: 1,
    padding: 16,
    marginHorizontal: 4,
    borderRadius: 8,
    alignItems: 'center',
    elevation: 2,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#8641f4',
  },
  statLabel: {
    fontSize: 12,
    opacity: 0.7,
  },
  card: {
    margin: 16,
    marginTop: 8,
  },
  cardTitle: {
    fontSize: 18,
    marginBottom: 16,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  companyItem: {
    marginBottom: 16,
  },
  companyInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  companyName: {
    fontWeight: 'bold',
  },
  companyStats: {
    fontSize: 12,
    opacity: 0.7,
  },
  progressBar: {
    height: 6,
    borderRadius: 3,
  },
  skillsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  skillChip: {
    margin: 4,
    backgroundColor: '#e3f2fd',
  },
  skillChipText: {
    color: '#1976d2',
  },
  actionButtons: {
    gap: 12,
  },
  actionButton: {
    marginBottom: 8,
  },
});
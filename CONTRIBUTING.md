# Contributing to Pixel Plant AI Companion 🌿

Thank you for your interest in contributing to the Pixel Plant project! We're building caring technology that genuinely supports human wellbeing, and we'd love your help making it even better.

## 🌟 Ways to Contribute

### 🔧 Code Contributions
- **Firmware Development**: Improve AI models, add features, optimize performance
- **Hardware Design**: Create PCB layouts, improve schematics, design enclosures
- **Documentation**: Write guides, improve existing docs, create video tutorials
- **Testing**: Report bugs, test on different hardware configurations

### 🎨 Creative Contributions  
- **Personality Development**: Create new response styles and character variations
- **Visual Design**: LED animation patterns, enclosure designs, community graphics
- **Community Building**: Help other makers, share your builds, organize workshops

### 🐛 Bug Reports & Feature Requests
- Use our [issue templates](.github/ISSUE_TEMPLATE/) for consistent reporting
- Include hardware configuration, software version, and reproduction steps
- Search existing issues before creating new ones

## 🚀 Getting Started

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/pixel-plant.git
   cd pixel-plant
   ```

2. **Set up development environment**
   - Install [Arduino IDE](https://www.arduino.cc/en/software)
   - Add ESP32 board support
   - Install required libraries (see README.md)

3. **Test your setup**
   ```bash
   # Compile example sketch
   arduino --verify firmware/examples/led_test/led_test.ino
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-awesome-feature
   ```

## 📝 Coding Standards

### Arduino/C++ Code Style
- **Indentation**: 2 spaces (no tabs)
- **Naming**: camelCase for functions, PascalCase for classes
- **Comments**: Explain why, not what
- **Constants**: ALL_CAPS with underscores

```cpp
// Good example
class PersonalityEngine {
private:
  const int MAX_MOOD_STATES = 5;
  
public:
  void updateMoodState(MoodType newMood) {
    // Update mood only if different to avoid unnecessary LED changes
    if (currentMood != newMood) {
      currentMood = newMood;
      displayMoodChange();
    }
  }
};
```

### Documentation Standards
- **Comments**: Use clear, concise explanations
- **Markdown**: Follow CommonMark specification
- **Examples**: Include working code examples
- **Images**: Use descriptive alt text and reasonable file sizes

### Git Commit Guidelines
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat: add voice recognition for wake commands
fix: resolve LED flickering during mood transitions  
docs: update assembly guide with new wiring diagram
test: add unit tests for personality response selection
```

## 🧪 Testing Requirements

### Before Submitting
- [ ] Code compiles without warnings
- [ ] Hardware tests pass (if applicable)
- [ ] Documentation is updated
- [ ] Examples work as described
- [ ] No sensitive information in commits

### Hardware Testing
- Test on actual ESP32-S3 hardware when possible
- Verify power consumption and thermal behavior
- Check all LED animations and audio output
- Validate sensor accuracy and responsiveness

## 📋 Pull Request Process

### 1. Preparation
- Sync with latest main branch
- Test your changes thoroughly
- Update documentation as needed
- Add or update examples if relevant

### 2. Create Pull Request
- Use our [PR template](.github/PULL_REQUEST_TEMPLATE.md)
- Reference related issues with "Fixes #123" or "Closes #123"
- Include screenshots/videos for hardware changes
- Describe testing performed

### 3. Review Process
- Maintainers will review within 48 hours
- Address feedback promptly and professionally
- Update your branch if conflicts arise
- Be patient - quality takes time!

## 🎯 Priority Areas

We especially welcome contributions in these areas:

### High Priority
- **AI Model Optimization**: Improve behavioral recognition accuracy
- **Power Management**: Extend battery life and reduce power consumption
- **User Experience**: Enhance personality responses and interactions
- **Documentation**: Assembly guides, troubleshooting, video tutorials

### Medium Priority
- **Hardware Variants**: Support for different sensors and displays
- **Customization Tools**: Easy personality and behavior configuration
- **Integration APIs**: Connect with health apps and smart home systems
- **Performance Testing**: Benchmarking and optimization

## 🌍 Community Guidelines

### Our Values
- **Caring Technology**: Everything we build should genuinely help people
- **Inclusive Community**: Welcome makers of all skill levels and backgrounds
- **Open Learning**: Share knowledge freely and support others' growth
- **Respectful Interaction**: Treat everyone with kindness and professionalism

### Code of Conduct
- **Be Respectful**: No harassment, discrimination, or toxic behavior
- **Be Helpful**: Support other community members with patience
- **Be Constructive**: Provide actionable feedback, not just criticism
- **Be Collaborative**: Work together toward shared goals

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community chat
- **Pull Requests**: Code review and technical discussion

## 🎓 Learning Resources

### New to Arduino/ESP32?
- [Arduino Getting Started Guide](https://www.arduino.cc/en/Guide)
- [ESP32 Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/)
- [Embedded AI Basics](https://www.tensorflow.org/lite/microcontrollers)

### New to Open Source?
- [First Contributions Guide](https://github.com/firstcontributions/first-contributions)
- [How to Write a Good Commit Message](https://chris.beams.io/posts/git-commit/)
- [Open Source Guide](https://opensource.guide/)

## 🏆 Recognition

### Contributor Wall
Active contributors are recognized in:
- README.md acknowledgments section
- Release notes for major contributions
- Community showcase for creative builds
- Annual contributor appreciation posts

### Special Recognition
- **First-time contributors**: Welcome badge and special thanks
- **Major features**: Highlighted in release announcements  
- **Community support**: Recognition for helping other makers
- **Documentation heroes**: Special appreciation for docs improvements

## 📞 Getting Help

### Stuck on Something?
1. Check existing documentation in `docs/`
2. Search closed issues for similar problems
3. Ask in GitHub Discussions
4. Reach out to maintainers for complex questions

### Maintainer Contact
- **Technical Questions**: Use GitHub Issues or Discussions
- **Security Issues**: See [SECURITY.md](SECURITY.md)
- **Community Issues**: Contact maintainers directly

## 🎉 Thank You!

Every contribution, no matter how small, helps build caring technology that makes people's lives better. Whether you fix a typo, submit a bug report, or build an amazing new feature, you're part of making the world a little more caring.

**Together, let's build technology that truly cares!** 🌟

---

*"The best contributions come from the heart—just like the Pixel Plant itself."*
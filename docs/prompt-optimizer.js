/**
 * Natural Language Parser
 * Converts natural language input into structured data
 */
class NaturalLanguageParser {
    constructor() {
        this.intentPatterns = [
            /(?:write|create|generate|make|build|develop)\s+(?:me\s+)?(?:a\s+)?(.+?)(?:\.|$)/i,
            /(?:explain|describe|tell me about)\s+(.+?)(?:\.|$)/i,
            /(?:help|assist|guide)\s+(?:me\s+)?(?:with|to)\s+(.+?)(?:\.|$)/i,
            /(?:i\s+)?(?:want|need|would like)\s+(?:to\s+)?(.+?)(?:\.|$)/i,
        ];
        
        this.requirementKeywords = [
            "should", "must", "need", "require", "include", 
            "with", "containing", "that", "having"
        ];
    }
    
    parse(text) {
        text = text.trim();
        
        return {
            intent: this._extractIntent(text),
            context: this._extractContext(text),
            requirements: this._extractRequirements(text),
            output_format: this._extractOutputFormat(text),
            original_text: text
        };
    }
    
    _extractIntent(text) {
        const textLower = text.toLowerCase();
        
        for (const pattern of this.intentPatterns) {
            const match = text.match(pattern);
            if (match) {
                let intent = match[1].trim();
                
                // Remove pronouns and unnecessary words
                intent = intent.replace(/^(me|us|you|for\s+me|for\s+us)\s+/i, '');
                intent = intent.replace(/^(a|an|the)\s+/i, '');
                
                // If intent is too short, try alternative patterns
                if (intent.split(' ').length <= 2 && intent.toLowerCase().includes('me')) {
                    const altPatterns = [
                        /(?:write|create|generate|make|build|develop)\s+(?:me\s+)?(?:a\s+)?(.+?)(?:\.|$)/i,
                        /(?:write|create|generate|make|build|develop)\s+(.+?)(?:\.|$)/i,
                    ];
                    
                    for (const altPattern of altPatterns) {
                        const altMatch = text.match(altPattern);
                        if (altMatch) {
                            intent = altMatch[1].trim();
                            intent = intent.replace(/^(me|us|you|for\s+me|for\s+us|a|an|the)\s+/i, '');
                            break;
                        }
                    }
                }
                
                return intent.trim();
            }
        }
        
        return text;
    }
    
    _extractContext(text) {
        const contextPatterns = [
            /given\s+(?:that\s+)?(.+?)(?:,|\.|\s+explain|\s+write|\s+create)/i,
            /assuming\s+(?:that\s+)?(.+?)(?:,|\.|\s+explain|\s+write|\s+create)/i,
            /for\s+(?:a\s+)?(.+?)(?:,|\.|\s+write|\s+create|\s+explain)/i,
            /(?:context|background|situation):\s*(.+?)(?:\.|$)/i,
            /as\s+(?:a\s+)?(.+?)(?:,|\.|\s+explain|\s+write)/i,
        ];
        
        for (const pattern of contextPatterns) {
            const match = text.match(pattern);
            if (match) {
                let context = match[1].trim();
                context = context.replace(/^(a|an|the)\s+/i, '');
                if (context.length > 3) {
                    return context;
                }
            }
        }
        
        return "";
    }
    
    _extractRequirements(text) {
        const requirements = [];
        
        // Look for requirement patterns
        for (const keyword of this.requirementKeywords) {
            const pattern = new RegExp(`(?:it|the|this)\\s+(?:should|must|need|require|include)\\s+(.+?)(?:\\.|,|$)`, 'gi');
            let match;
            while ((match = pattern.exec(text)) !== null) {
                const req = match[1].trim();
                if (req) {
                    requirements.push(req);
                }
            }
        }
        
        // Look for list-like requirements
        const listPattern = /(?:should|must|need)\s+be\s+(.+?)(?:\.|$)/gi;
        let match;
        while ((match = listPattern.exec(text)) !== null) {
            const req = match[1].trim();
            if (req) {
                requirements.push(req);
            }
        }
        
        // Remove duplicates
        return [...new Set(requirements)];
    }
    
    _extractOutputFormat(text) {
        const textLower = text.toLowerCase();
        
        // Direct format mentions
        const directFormats = ["json", "xml", "markdown", "html", "csv", "yaml"];
        for (const fmt of directFormats) {
            if (textLower.includes(fmt)) {
                const formatPattern = new RegExp(`(?:in|as|with|using)\\s+(?:a|an)?\\s*${fmt}`, 'i');
                if (formatPattern.test(textLower)) {
                    return fmt;
                }
            }
        }
        
        // Format type patterns
        const formatPatterns = [
            /(?:in|as|with|using)\s+(?:a|an)?\s*(?:output\s+)?(?:format|structure|style|type|form)\s+(?:of\s+)?(.+?)(?:\.|$)/i,
            /(?:format|structure|style)\s*:\s*(.+?)(?:\.|$)/i,
        ];
        
        for (const pattern of formatPatterns) {
            const match = text.match(pattern);
            if (match) {
                const formatDesc = match[1].trim().toLowerCase();
                if (formatDesc !== "format") {
                    return formatDesc;
                }
            }
        }
        
        return "";
    }
}

/**
 * Prompt Optimizer
 * Builds optimized prompts following OpenAI's best practices
 */
class PromptOptimizer {
    constructor() {
        this.parser = new NaturalLanguageParser();
    }
    
    optimize(naturalLanguageText) {
        const parsedData = this.parser.parse(naturalLanguageText);
        return this._buildPrompt(parsedData);
    }
    
    _buildPrompt(parsedData) {
        const { intent, context, requirements, output_format, original_text } = parsedData;
        
        const isComplex = this._isComplexTask(intent, requirements);
        const role = this._determineRole(intent);
        
        const promptParts = [];
        
        // 1. Role assignment
        if (role) {
            promptParts.push(`You are ${role}.`);
        }
        
        // 2. Main instruction with delimiters
        const mainInstruction = this._createMainInstruction(intent, original_text);
        promptParts.push(mainInstruction);
        
        // 3. Context with delimiters
        if (context) {
            promptParts.push(`\nContext:\n"""${context}"""`);
        }
        
        // 4. Requirements
        if (requirements.length > 0) {
            promptParts.push("\nRequirements:");
            requirements.forEach(req => {
                promptParts.push(`- ${req}`);
            });
        }
        
        // 5. Chain-of-thought for complex tasks
        if (isComplex) {
            const steps = this._generateSteps(intent, requirements);
            if (steps.length > 0) {
                promptParts.push("\nPlease follow these steps:");
                steps.forEach((step, index) => {
                    promptParts.push(`${index + 1}. ${step}`);
                });
            }
        }
        
        // 6. Output format specification
        const formatSpec = this._createOutputFormatSpec(output_format, intent);
        if (formatSpec) {
            promptParts.push(`\n${formatSpec}`);
        }
        
        // 7. Additional best practices
        promptParts.push("\nPlease be specific, clear, and comprehensive in your response.");
        
        return promptParts.join("\n");
    }
    
    _isComplexTask(intent, requirements) {
        const complexIndicators = [
            "analyze", "create", "build", "develop", "design", "write",
            "report", "plan", "explain", "compare", "evaluate"
        ];
        
        const intentLower = intent.toLowerCase();
        const hasComplexIndicator = complexIndicators.some(indicator => 
            intentLower.includes(indicator)
        );
        const hasMultipleRequirements = requirements.length >= 2;
        
        return hasComplexIndicator || hasMultipleRequirements;
    }
    
    _determineRole(intent) {
        const intentLower = intent.toLowerCase();
        
        const roleMappings = {
            "story": "an expert creative writer",
            "write": "an expert writer",
            "explain": "an expert educator",
            "analyze": "an expert data analyst",
            "code": "an expert software developer",
            "design": "an expert designer",
            "plan": "an expert strategist",
            "report": "an expert analyst",
            "create": "a creative professional",
        };
        
        for (const [keyword, role] of Object.entries(roleMappings)) {
            if (intentLower.includes(keyword)) {
                return role;
            }
        }
        
        return "an expert assistant";
    }
    
    _createMainInstruction(intent, originalText) {
        if (originalText && originalText.length > intent.length + 10) {
            return `Please complete the following task:\n\n"""${originalText}"""`;
        } else {
            return `Task: ${intent}.`;
        }
    }
    
    _generateSteps(intent, requirements) {
        const intentLower = intent.toLowerCase();
        
        if (intentLower.includes("write") || intentLower.includes("story")) {
            return [
                "Plan the structure and key elements",
                "Develop the content with clear narrative",
                "Review and refine for clarity and engagement"
            ];
        } else if (intentLower.includes("analyze") || intentLower.includes("report")) {
            return [
                "Identify key data points and information",
                "Analyze patterns and relationships",
                "Present findings in a clear, structured format"
            ];
        } else if (intentLower.includes("explain")) {
            return [
                "Break down the concept into understandable parts",
                "Provide examples and analogies",
                "Summarize key takeaways"
            ];
        } else if (intentLower.includes("create") || intentLower.includes("build")) {
            return [
                "Define the requirements and scope",
                "Design the approach or structure",
                "Implement the solution step by step"
            ];
        } else {
            return [
                "Understand the requirements",
                "Break down into manageable components",
                "Execute systematically"
            ];
        }
    }
    
    _createOutputFormatSpec(outputFormat, intent) {
        if (outputFormat) {
            return `Output Format: Provide your response in ${outputFormat} format.`;
        }
        
        const intentLower = intent.toLowerCase();
        const formatHints = {
            "story": "narrative format with clear paragraphs",
            "report": "structured format with sections and headings",
            "list": "bulleted or numbered list format",
            "code": "code format with syntax highlighting",
            "explain": "clear explanation with examples",
            "analyze": "analysis format with findings and conclusions"
        };
        
        for (const [keyword, formatDesc] of Object.entries(formatHints)) {
            if (intentLower.includes(keyword)) {
                return `Output Format: Provide your response in ${formatDesc}.`;
            }
        }
        
        return "";
    }
}


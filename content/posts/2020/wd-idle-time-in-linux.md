---
type: "post"
aliases:
- /2020/01/wd-idle-time-in-linux.html
date: "2020-01-07T00:00:00Z"
tags:
- linux
- fedora
title: Values for WD idle time in Linux
---

There is a tool called idle3ctl which can disable, get or set the idle3 timer
on Western Digital hard drives. Idle3ctl can be used as an alternative to the
official wdidle3.exe proprietary utility, without the need to reboot in a DOS
environement. Idle3ctl is an independant project, unrelated in any way to
Western Digital Corp.

To set idle3 timer raw value, option -s must be used. Value must be an integer
between 1 and 255. The idle3 timer is set in  0.1s for the 1-128 range, and
in 30s for the 129-255 range. Example:

    # idle3ctl -s190 /dev/sdc
    Idle3 timer set to 190 (0xbe)
    Please power cycle your drive off and on for the new
    setting to be taken into account. A reboot will not be enough!

    # idle3ctl -g /dev/sdc
    Idle3 timer set to 190 (0xbe)

Here is the snag, I had to do some math to be able to figure out the correct
value. So I created a table for you, so you don't have to! Enjoy.

<!--more-->

<p>
<table class="blueTable">
    <thead>
        <tr>
            <td>Value</td>
            <td>Seconds</td>
            <td>Minutes</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>0.10</td>
            <td>0.00</td>
        </tr>
        <tr>
            <td>2</td>
            <td>0.20</td>
            <td>0.00</td>
        </tr>
        <tr>
            <td>3</td>
            <td>0.30</td>
            <td>0.01</td>
        </tr>
        <tr>
            <td>4</td>
            <td>0.40</td>
            <td>0.01</td>
        </tr>
        <tr>
            <td>5</td>
            <td>0.50</td>
            <td>0.01</td>
        </tr>
        <tr>
            <td>6</td>
            <td>0.60</td>
            <td>0.01</td>
        </tr>
        <tr>
            <td>7</td>
            <td>0.70</td>
            <td>0.01</td>
        </tr>
        <tr>
            <td>8</td>
            <td>0.80</td>
            <td>0.01</td>
        </tr>
        <tr>
            <td>9</td>
            <td>0.90</td>
            <td>0.02</td>
        </tr>
        <tr>
            <td>10</td>
            <td>1.00</td>
            <td>0.02</td>
        </tr>
        <tr>
            <td>11</td>
            <td>1.10</td>
            <td>0.02</td>
        </tr>
        <tr>
            <td>12</td>
            <td>1.20</td>
            <td>0.02</td>
        </tr>
        <tr>
            <td>13</td>
            <td>1.30</td>
            <td>0.02</td>
        </tr>
        <tr>
            <td>14</td>
            <td>1.40</td>
            <td>0.02</td>
        </tr>
        <tr>
            <td>15</td>
            <td>1.50</td>
            <td>0.03</td>
        </tr>
        <tr>
            <td>16</td>
            <td>1.60</td>
            <td>0.03</td>
        </tr>
        <tr>
            <td>17</td>
            <td>1.70</td>
            <td>0.03</td>
        </tr>
        <tr>
            <td>18</td>
            <td>1.80</td>
            <td>0.03</td>
        </tr>
        <tr>
            <td>19</td>
            <td>1.90</td>
            <td>0.03</td>
        </tr>
        <tr>
            <td>20</td>
            <td>2.00</td>
            <td>0.03</td>
        </tr>
        <tr>
            <td>21</td>
            <td>2.10</td>
            <td>0.04</td>
        </tr>
        <tr>
            <td>22</td>
            <td>2.20</td>
            <td>0.04</td>
        </tr>
        <tr>
            <td>23</td>
            <td>2.30</td>
            <td>0.04</td>
        </tr>
        <tr>
            <td>24</td>
            <td>2.40</td>
            <td>0.04</td>
        </tr>
        <tr>
            <td>25</td>
            <td>2.50</td>
            <td>0.04</td>
        </tr>
        <tr>
            <td>26</td>
            <td>2.60</td>
            <td>0.04</td>
        </tr>
        <tr>
            <td>27</td>
            <td>2.70</td>
            <td>0.05</td>
        </tr>
        <tr>
            <td>28</td>
            <td>2.80</td>
            <td>0.05</td>
        </tr>
        <tr>
            <td>29</td>
            <td>2.90</td>
            <td>0.05</td>
        </tr>
        <tr>
            <td>30</td>
            <td>3.00</td>
            <td>0.05</td>
        </tr>
        <tr>
            <td>31</td>
            <td>3.10</td>
            <td>0.05</td>
        </tr>
        <tr>
            <td>32</td>
            <td>3.20</td>
            <td>0.05</td>
        </tr>
        <tr>
            <td>33</td>
            <td>3.30</td>
            <td>0.06</td>
        </tr>
        <tr>
            <td>34</td>
            <td>3.40</td>
            <td>0.06</td>
        </tr>
        <tr>
            <td>35</td>
            <td>3.50</td>
            <td>0.06</td>
        </tr>
        <tr>
            <td>36</td>
            <td>3.60</td>
            <td>0.06</td>
        </tr>
        <tr>
            <td>37</td>
            <td>3.70</td>
            <td>0.06</td>
        </tr>
        <tr>
            <td>38</td>
            <td>3.80</td>
            <td>0.06</td>
        </tr>
        <tr>
            <td>39</td>
            <td>3.90</td>
            <td>0.07</td>
        </tr>
        <tr>
            <td>40</td>
            <td>4.00</td>
            <td>0.07</td>
        </tr>
        <tr>
            <td>41</td>
            <td>4.10</td>
            <td>0.07</td>
        </tr>
        <tr>
            <td>42</td>
            <td>4.20</td>
            <td>0.07</td>
        </tr>
        <tr>
            <td>43</td>
            <td>4.30</td>
            <td>0.07</td>
        </tr>
        <tr>
            <td>44</td>
            <td>4.40</td>
            <td>0.07</td>
        </tr>
        <tr>
            <td>45</td>
            <td>4.50</td>
            <td>0.08</td>
        </tr>
        <tr>
            <td>46</td>
            <td>4.60</td>
            <td>0.08</td>
        </tr>
        <tr>
            <td>47</td>
            <td>4.70</td>
            <td>0.08</td>
        </tr>
        <tr>
            <td>48</td>
            <td>4.80</td>
            <td>0.08</td>
        </tr>
        <tr>
            <td>49</td>
            <td>4.90</td>
            <td>0.08</td>
        </tr>
        <tr>
            <td>50</td>
            <td>5.00</td>
            <td>0.08</td>
        </tr>
        <tr>
            <td>51</td>
            <td>5.10</td>
            <td>0.08</td>
        </tr>
        <tr>
            <td>52</td>
            <td>5.20</td>
            <td>0.09</td>
        </tr>
        <tr>
            <td>53</td>
            <td>5.30</td>
            <td>0.09</td>
        </tr>
        <tr>
            <td>54</td>
            <td>5.40</td>
            <td>0.09</td>
        </tr>
        <tr>
            <td>55</td>
            <td>5.50</td>
            <td>0.09</td>
        </tr>
        <tr>
            <td>56</td>
            <td>5.60</td>
            <td>0.09</td>
        </tr>
        <tr>
            <td>57</td>
            <td>5.70</td>
            <td>0.09</td>
        </tr>
        <tr>
            <td>58</td>
            <td>5.80</td>
            <td>0.10</td>
        </tr>
        <tr>
            <td>59</td>
            <td>5.90</td>
            <td>0.10</td>
        </tr>
        <tr>
            <td>60</td>
            <td>6.00</td>
            <td>0.10</td>
        </tr>
        <tr>
            <td>61</td>
            <td>6.10</td>
            <td>0.10</td>
        </tr>
        <tr>
            <td>62</td>
            <td>6.20</td>
            <td>0.10</td>
        </tr>
        <tr>
            <td>63</td>
            <td>6.30</td>
            <td>0.11</td>
        </tr>
        <tr>
            <td>64</td>
            <td>6.40</td>
            <td>0.11</td>
        </tr>
        <tr>
            <td>65</td>
            <td>6.50</td>
            <td>0.11</td>
        </tr>
        <tr>
            <td>66</td>
            <td>6.60</td>
            <td>0.11</td>
        </tr>
        <tr>
            <td>67</td>
            <td>6.70</td>
            <td>0.11</td>
        </tr>
        <tr>
            <td>68</td>
            <td>6.80</td>
            <td>0.11</td>
        </tr>
        <tr>
            <td>69</td>
            <td>6.90</td>
            <td>0.12</td>
        </tr>
        <tr>
            <td>70</td>
            <td>7.00</td>
            <td>0.12</td>
        </tr>
        <tr>
            <td>71</td>
            <td>7.10</td>
            <td>0.12</td>
        </tr>
        <tr>
            <td>72</td>
            <td>7.20</td>
            <td>0.12</td>
        </tr>
        <tr>
            <td>73</td>
            <td>7.30</td>
            <td>0.12</td>
        </tr>
        <tr>
            <td>74</td>
            <td>7.40</td>
            <td>0.12</td>
        </tr>
        <tr>
            <td>75</td>
            <td>7.50</td>
            <td>0.13</td>
        </tr>
        <tr>
            <td>76</td>
            <td>7.60</td>
            <td>0.13</td>
        </tr>
        <tr>
            <td>77</td>
            <td>7.70</td>
            <td>0.13</td>
        </tr>
        <tr>
            <td>78</td>
            <td>7.80</td>
            <td>0.13</td>
        </tr>
        <tr>
            <td>79</td>
            <td>7.90</td>
            <td>0.13</td>
        </tr>
        <tr>
            <td>80</td>
            <td>8.00</td>
            <td>0.13</td>
        </tr>
        <tr>
            <td>81</td>
            <td>8.10</td>
            <td>0.14</td>
        </tr>
        <tr>
            <td>82</td>
            <td>8.20</td>
            <td>0.14</td>
        </tr>
        <tr>
            <td>83</td>
            <td>8.30</td>
            <td>0.14</td>
        </tr>
        <tr>
            <td>84</td>
            <td>8.40</td>
            <td>0.14</td>
        </tr>
        <tr>
            <td>85</td>
            <td>8.50</td>
            <td>0.14</td>
        </tr>
        <tr>
            <td>86</td>
            <td>8.60</td>
            <td>0.14</td>
        </tr>
        <tr>
            <td>87</td>
            <td>8.70</td>
            <td>0.15</td>
        </tr>
        <tr>
            <td>88</td>
            <td>8.80</td>
            <td>0.15</td>
        </tr>
        <tr>
            <td>89</td>
            <td>8.90</td>
            <td>0.15</td>
        </tr>
        <tr>
            <td>90</td>
            <td>9.00</td>
            <td>0.15</td>
        </tr>
        <tr>
            <td>91</td>
            <td>9.10</td>
            <td>0.15</td>
        </tr>
        <tr>
            <td>92</td>
            <td>9.20</td>
            <td>0.15</td>
        </tr>
        <tr>
            <td>93</td>
            <td>9.30</td>
            <td>0.16</td>
        </tr>
        <tr>
            <td>94</td>
            <td>9.40</td>
            <td>0.16</td>
        </tr>
        <tr>
            <td>95</td>
            <td>9.50</td>
            <td>0.16</td>
        </tr>
        <tr>
            <td>96</td>
            <td>9.60</td>
            <td>0.16</td>
        </tr>
        <tr>
            <td>97</td>
            <td>9.70</td>
            <td>0.16</td>
        </tr>
        <tr>
            <td>98</td>
            <td>9.80</td>
            <td>0.16</td>
        </tr>
        <tr>
            <td>99</td>
            <td>9.90</td>
            <td>0.17</td>
        </tr>
        <tr>
            <td>100</td>
            <td>10.00</td>
            <td>0.17</td>
        </tr>
        <tr>
            <td>101</td>
            <td>10.10</td>
            <td>0.17</td>
        </tr>
        <tr>
            <td>102</td>
            <td>10.20</td>
            <td>0.17</td>
        </tr>
        <tr>
            <td>103</td>
            <td>10.30</td>
            <td>0.17</td>
        </tr>
        <tr>
            <td>104</td>
            <td>10.40</td>
            <td>0.17</td>
        </tr>
        <tr>
            <td>105</td>
            <td>10.50</td>
            <td>0.18</td>
        </tr>
        <tr>
            <td>106</td>
            <td>10.60</td>
            <td>0.18</td>
        </tr>
        <tr>
            <td>107</td>
            <td>10.70</td>
            <td>0.18</td>
        </tr>
        <tr>
            <td>108</td>
            <td>10.80</td>
            <td>0.18</td>
        </tr>
        <tr>
            <td>109</td>
            <td>10.90</td>
            <td>0.18</td>
        </tr>
        <tr>
            <td>110</td>
            <td>11.00</td>
            <td>0.18</td>
        </tr>
        <tr>
            <td>111</td>
            <td>11.10</td>
            <td>0.19</td>
        </tr>
        <tr>
            <td>112</td>
            <td>11.20</td>
            <td>0.19</td>
        </tr>
        <tr>
            <td>113</td>
            <td>11.30</td>
            <td>0.19</td>
        </tr>
        <tr>
            <td>114</td>
            <td>11.40</td>
            <td>0.19</td>
        </tr>
        <tr>
            <td>115</td>
            <td>11.50</td>
            <td>0.19</td>
        </tr>
        <tr>
            <td>116</td>
            <td>11.60</td>
            <td>0.19</td>
        </tr>
        <tr>
            <td>117</td>
            <td>11.70</td>
            <td>0.20</td>
        </tr>
        <tr>
            <td>118</td>
            <td>11.80</td>
            <td>0.20</td>
        </tr>
        <tr>
            <td>119</td>
            <td>11.90</td>
            <td>0.20</td>
        </tr>
        <tr>
            <td>120</td>
            <td>12.00</td>
            <td>0.20</td>
        </tr>
        <tr>
            <td>121</td>
            <td>12.10</td>
            <td>0.20</td>
        </tr>
        <tr>
            <td>122</td>
            <td>12.20</td>
            <td>0.20</td>
        </tr>
        <tr>
            <td>123</td>
            <td>12.30</td>
            <td>0.21</td>
        </tr>
        <tr>
            <td>124</td>
            <td>12.40</td>
            <td>0.21</td>
        </tr>
        <tr>
            <td>125</td>
            <td>12.50</td>
            <td>0.21</td>
        </tr>
        <tr>
            <td>126</td>
            <td>12.60</td>
            <td>0.21</td>
        </tr>
        <tr>
            <td>127</td>
            <td>12.70</td>
            <td>0.21</td>
        </tr>
        <tr>
            <td>128</td>
            <td>12.80</td>
            <td>0.21</td>
        </tr>
        <tr>
            <td>129</td>
            <td>42.80</td>
            <td>0.71</td>
        </tr>
        <tr>
            <td>130</td>
            <td>72.80</td>
            <td>1.21</td>
        </tr>
        <tr>
            <td>131</td>
            <td>102.80</td>
            <td>1.71</td>
        </tr>
        <tr>
            <td>132</td>
            <td>132.80</td>
            <td>2.21</td>
        </tr>
        <tr>
            <td>133</td>
            <td>162.80</td>
            <td>2.71</td>
        </tr>
        <tr>
            <td>134</td>
            <td>192.80</td>
            <td>3.21</td>
        </tr>
        <tr>
            <td>135</td>
            <td>222.80</td>
            <td>3.71</td>
        </tr>
        <tr>
            <td>136</td>
            <td>252.80</td>
            <td>4.21</td>
        </tr>
        <tr>
            <td>137</td>
            <td>282.80</td>
            <td>4.71</td>
        </tr>
        <tr>
            <td>138</td>
            <td>312.80</td>
            <td>5.21</td>
        </tr>
        <tr>
            <td>139</td>
            <td>342.80</td>
            <td>5.71</td>
        </tr>
        <tr>
            <td>140</td>
            <td>372.80</td>
            <td>6.21</td>
        </tr>
        <tr>
            <td>141</td>
            <td>402.80</td>
            <td>6.71</td>
        </tr>
        <tr>
            <td>142</td>
            <td>432.80</td>
            <td>7.21</td>
        </tr>
        <tr>
            <td>143</td>
            <td>462.80</td>
            <td>7.71</td>
        </tr>
        <tr>
            <td>144</td>
            <td>492.80</td>
            <td>8.21</td>
        </tr>
        <tr>
            <td>145</td>
            <td>522.80</td>
            <td>8.71</td>
        </tr>
        <tr>
            <td>146</td>
            <td>552.80</td>
            <td>9.21</td>
        </tr>
        <tr>
            <td>147</td>
            <td>582.80</td>
            <td>9.71</td>
        </tr>
        <tr>
            <td>148</td>
            <td>612.80</td>
            <td>10.21</td>
        </tr>
        <tr>
            <td>149</td>
            <td>642.80</td>
            <td>10.71</td>
        </tr>
        <tr>
            <td>150</td>
            <td>672.80</td>
            <td>11.21</td>
        </tr>
        <tr>
            <td>151</td>
            <td>702.80</td>
            <td>11.71</td>
        </tr>
        <tr>
            <td>152</td>
            <td>732.80</td>
            <td>12.21</td>
        </tr>
        <tr>
            <td>153</td>
            <td>762.80</td>
            <td>12.71</td>
        </tr>
        <tr>
            <td>154</td>
            <td>792.80</td>
            <td>13.21</td>
        </tr>
        <tr>
            <td>155</td>
            <td>822.80</td>
            <td>13.71</td>
        </tr>
        <tr>
            <td>156</td>
            <td>852.80</td>
            <td>14.21</td>
        </tr>
        <tr>
            <td>157</td>
            <td>882.80</td>
            <td>14.71</td>
        </tr>
        <tr>
            <td>158</td>
            <td>912.80</td>
            <td>15.21</td>
        </tr>
        <tr>
            <td>159</td>
            <td>942.80</td>
            <td>15.71</td>
        </tr>
        <tr>
            <td>160</td>
            <td>972.80</td>
            <td>16.21</td>
        </tr>
        <tr>
            <td>161</td>
            <td>1002.80</td>
            <td>16.71</td>
        </tr>
        <tr>
            <td>162</td>
            <td>1032.80</td>
            <td>17.21</td>
        </tr>
        <tr>
            <td>163</td>
            <td>1062.80</td>
            <td>17.71</td>
        </tr>
        <tr>
            <td>164</td>
            <td>1092.80</td>
            <td>18.21</td>
        </tr>
        <tr>
            <td>165</td>
            <td>1122.80</td>
            <td>18.71</td>
        </tr>
        <tr>
            <td>166</td>
            <td>1152.80</td>
            <td>19.21</td>
        </tr>
        <tr>
            <td>167</td>
            <td>1182.80</td>
            <td>19.71</td>
        </tr>
        <tr>
            <td>168</td>
            <td>1212.80</td>
            <td>20.21</td>
        </tr>
        <tr>
            <td>169</td>
            <td>1242.80</td>
            <td>20.71</td>
        </tr>
        <tr>
            <td>170</td>
            <td>1272.80</td>
            <td>21.21</td>
        </tr>
        <tr>
            <td>171</td>
            <td>1302.80</td>
            <td>21.71</td>
        </tr>
        <tr>
            <td>172</td>
            <td>1332.80</td>
            <td>22.21</td>
        </tr>
        <tr>
            <td>173</td>
            <td>1362.80</td>
            <td>22.71</td>
        </tr>
        <tr>
            <td>174</td>
            <td>1392.80</td>
            <td>23.21</td>
        </tr>
        <tr>
            <td>175</td>
            <td>1422.80</td>
            <td>23.71</td>
        </tr>
        <tr>
            <td>176</td>
            <td>1452.80</td>
            <td>24.21</td>
        </tr>
        <tr>
            <td>177</td>
            <td>1482.80</td>
            <td>24.71</td>
        </tr>
        <tr>
            <td>178</td>
            <td>1512.80</td>
            <td>25.21</td>
        </tr>
        <tr>
            <td>179</td>
            <td>1542.80</td>
            <td>25.71</td>
        </tr>
        <tr>
            <td>180</td>
            <td>1572.80</td>
            <td>26.21</td>
        </tr>
        <tr>
            <td>181</td>
            <td>1602.80</td>
            <td>26.71</td>
        </tr>
        <tr>
            <td>182</td>
            <td>1632.80</td>
            <td>27.21</td>
        </tr>
        <tr>
            <td>183</td>
            <td>1662.80</td>
            <td>27.71</td>
        </tr>
        <tr>
            <td>184</td>
            <td>1692.80</td>
            <td>28.21</td>
        </tr>
        <tr>
            <td>185</td>
            <td>1722.80</td>
            <td>28.71</td>
        </tr>
        <tr>
            <td>186</td>
            <td>1752.80</td>
            <td>29.21</td>
        </tr>
        <tr>
            <td>187</td>
            <td>1782.80</td>
            <td>29.71</td>
        </tr>
        <tr>
            <td>188</td>
            <td>1812.80</td>
            <td>30.21</td>
        </tr>
        <tr>
            <td>189</td>
            <td>1842.80</td>
            <td>30.71</td>
        </tr>
        <tr>
            <td>190</td>
            <td>1872.80</td>
            <td>31.21</td>
        </tr>
        <tr>
            <td>191</td>
            <td>1902.80</td>
            <td>31.71</td>
        </tr>
        <tr>
            <td>192</td>
            <td>1932.80</td>
            <td>32.21</td>
        </tr>
        <tr>
            <td>193</td>
            <td>1962.80</td>
            <td>32.71</td>
        </tr>
        <tr>
            <td>194</td>
            <td>1992.80</td>
            <td>33.21</td>
        </tr>
        <tr>
            <td>195</td>
            <td>2022.80</td>
            <td>33.71</td>
        </tr>
        <tr>
            <td>196</td>
            <td>2052.80</td>
            <td>34.21</td>
        </tr>
        <tr>
            <td>197</td>
            <td>2082.80</td>
            <td>34.71</td>
        </tr>
        <tr>
            <td>198</td>
            <td>2112.80</td>
            <td>35.21</td>
        </tr>
        <tr>
            <td>199</td>
            <td>2142.80</td>
            <td>35.71</td>
        </tr>
        <tr>
            <td>200</td>
            <td>2172.80</td>
            <td>36.21</td>
        </tr>
        <tr>
            <td>201</td>
            <td>2202.80</td>
            <td>36.71</td>
        </tr>
        <tr>
            <td>202</td>
            <td>2232.80</td>
            <td>37.21</td>
        </tr>
        <tr>
            <td>203</td>
            <td>2262.80</td>
            <td>37.71</td>
        </tr>
        <tr>
            <td>204</td>
            <td>2292.80</td>
            <td>38.21</td>
        </tr>
        <tr>
            <td>205</td>
            <td>2322.80</td>
            <td>38.71</td>
        </tr>
        <tr>
            <td>206</td>
            <td>2352.80</td>
            <td>39.21</td>
        </tr>
        <tr>
            <td>207</td>
            <td>2382.80</td>
            <td>39.71</td>
        </tr>
        <tr>
            <td>208</td>
            <td>2412.80</td>
            <td>40.21</td>
        </tr>
        <tr>
            <td>209</td>
            <td>2442.80</td>
            <td>40.71</td>
        </tr>
        <tr>
            <td>210</td>
            <td>2472.80</td>
            <td>41.21</td>
        </tr>
        <tr>
            <td>211</td>
            <td>2502.80</td>
            <td>41.71</td>
        </tr>
        <tr>
            <td>212</td>
            <td>2532.80</td>
            <td>42.21</td>
        </tr>
        <tr>
            <td>213</td>
            <td>2562.80</td>
            <td>42.71</td>
        </tr>
        <tr>
            <td>214</td>
            <td>2592.80</td>
            <td>43.21</td>
        </tr>
        <tr>
            <td>215</td>
            <td>2622.80</td>
            <td>43.71</td>
        </tr>
        <tr>
            <td>216</td>
            <td>2652.80</td>
            <td>44.21</td>
        </tr>
        <tr>
            <td>217</td>
            <td>2682.80</td>
            <td>44.71</td>
        </tr>
        <tr>
            <td>218</td>
            <td>2712.80</td>
            <td>45.21</td>
        </tr>
        <tr>
            <td>219</td>
            <td>2742.80</td>
            <td>45.71</td>
        </tr>
        <tr>
            <td>220</td>
            <td>2772.80</td>
            <td>46.21</td>
        </tr>
        <tr>
            <td>221</td>
            <td>2802.80</td>
            <td>46.71</td>
        </tr>
        <tr>
            <td>222</td>
            <td>2832.80</td>
            <td>47.21</td>
        </tr>
        <tr>
            <td>223</td>
            <td>2862.80</td>
            <td>47.71</td>
        </tr>
        <tr>
            <td>224</td>
            <td>2892.80</td>
            <td>48.21</td>
        </tr>
        <tr>
            <td>225</td>
            <td>2922.80</td>
            <td>48.71</td>
        </tr>
        <tr>
            <td>226</td>
            <td>2952.80</td>
            <td>49.21</td>
        </tr>
        <tr>
            <td>227</td>
            <td>2982.80</td>
            <td>49.71</td>
        </tr>
        <tr>
            <td>228</td>
            <td>3012.80</td>
            <td>50.21</td>
        </tr>
        <tr>
            <td>229</td>
            <td>3042.80</td>
            <td>50.71</td>
        </tr>
        <tr>
            <td>230</td>
            <td>3072.80</td>
            <td>51.21</td>
        </tr>
        <tr>
            <td>231</td>
            <td>3102.80</td>
            <td>51.71</td>
        </tr>
        <tr>
            <td>232</td>
            <td>3132.80</td>
            <td>52.21</td>
        </tr>
        <tr>
            <td>233</td>
            <td>3162.80</td>
            <td>52.71</td>
        </tr>
        <tr>
            <td>234</td>
            <td>3192.80</td>
            <td>53.21</td>
        </tr>
        <tr>
            <td>235</td>
            <td>3222.80</td>
            <td>53.71</td>
        </tr>
        <tr>
            <td>236</td>
            <td>3252.80</td>
            <td>54.21</td>
        </tr>
        <tr>
            <td>237</td>
            <td>3282.80</td>
            <td>54.71</td>
        </tr>
        <tr>
            <td>238</td>
            <td>3312.80</td>
            <td>55.21</td>
        </tr>
        <tr>
            <td>239</td>
            <td>3342.80</td>
            <td>55.71</td>
        </tr>
        <tr>
            <td>240</td>
            <td>3372.80</td>
            <td>56.21</td>
        </tr>
        <tr>
            <td>241</td>
            <td>3402.80</td>
            <td>56.71</td>
        </tr>
        <tr>
            <td>242</td>
            <td>3432.80</td>
            <td>57.21</td>
        </tr>
        <tr>
            <td>243</td>
            <td>3462.80</td>
            <td>57.71</td>
        </tr>
        <tr>
            <td>244</td>
            <td>3492.80</td>
            <td>58.21</td>
        </tr>
        <tr>
            <td>245</td>
            <td>3522.80</td>
            <td>58.71</td>
        </tr>
        <tr>
            <td>246</td>
            <td>3552.80</td>
            <td>59.21</td>
        </tr>
        <tr>
            <td>247</td>
            <td>3582.80</td>
            <td>59.71</td>
        </tr>
        <tr>
            <td>248</td>
            <td>3612.80</td>
            <td>60.21</td>
        </tr>
        <tr>
            <td>249</td>
            <td>3642.80</td>
            <td>60.71</td>
        </tr>
        <tr>
            <td>250</td>
            <td>3672.80</td>
            <td>61.21</td>
        </tr>
        <tr>
            <td>251</td>
            <td>3702.80</td>
            <td>61.71</td>
        </tr>
        <tr>
            <td>252</td>
            <td>3732.80</td>
            <td>62.21</td>
        </tr>
        <tr>
            <td>253</td>
            <td>3762.80</td>
            <td>62.71</td>
        </tr>
        <tr>
            <td>254</td>
            <td>3792.80</td>
            <td>63.21</td>
        </tr>
        <tr>
            <td>255</td>
            <td>3822.80</td>
            <td>63.71</td>
        </tr>
    </tbody>
</table>
</p>

Alternatively, the same can be achieved via `smartctl` tool. Read my next
article about how to do that.

That's all. Good luck not breaking your drive! :-)